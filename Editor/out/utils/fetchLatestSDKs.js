"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getSDKVersions = exports.ensureSDKsUpToDate = exports.fetchLatestSDKs = void 0;
const vscode = __importStar(require("vscode"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const os = __importStar(require("os"));
const https = __importStar(require("https"));
const url_1 = require("url");
const stream_1 = require("stream");
const util_1 = require("util");
// eslint-disable-next-line @typescript-eslint/no-var-requires
const extract = require('extract-zip');
const streamPipeline = (0, util_1.promisify)(stream_1.pipeline);
const DEFAULT_POHLANG_REPO = { owner: 'AlhaqGH', repo: 'PohLang' };
const DEFAULT_PLHUB_REPO = { owner: 'AlhaqGH', repo: 'PLHub' };
function getConfig() {
    const cfg = vscode.workspace.getConfiguration('pohlangHub');
    // Support both old and new keys
    const pohRepoStr = cfg.get('pohlangRepo')
        || cfg.get('interpreterRepo')
        || `${DEFAULT_POHLANG_REPO.owner}/${DEFAULT_POHLANG_REPO.repo}`;
    const plRepoStr = cfg.get('plhubRepo')
        || cfg.get('sdkRepo')
        || `${DEFAULT_PLHUB_REPO.owner}/${DEFAULT_PLHUB_REPO.repo}`;
    const pohlangRepo = pohRepoStr.split('/');
    const plhubRepo = plRepoStr.split('/');
    const tagOverride = cfg.get('sdkTagOverride');
    const assetPattern = cfg.get('assetPattern');
    const updateIntervalDays = cfg.get('updateIntervalDays')
        ?? cfg.get('sdkUpdateIntervalDays')
        ?? 7;
    const autoUpdate = cfg.get('autoUpdate')
        ?? cfg.get('autoUpdateSDKs')
        ?? true;
    const githubToken = cfg.get('githubToken') || '';
    return {
        pohlangRepo: { owner: pohlangRepo[0], repo: pohlangRepo[1] },
        plhubRepo: { owner: plhubRepo[0], repo: plhubRepo[1] },
        tagOverride,
        assetPattern: assetPattern ? new RegExp(assetPattern, 'i') : undefined,
        updateIntervalDays,
        autoUpdate,
        githubToken,
    };
}
function buildRequestHeaders(token, extra) {
    const headers = {
        'User-Agent': 'PLHub-extension',
        ...extra,
    };
    if (token)
        headers['Authorization'] = `token ${token}`;
    return headers;
}
const REDIRECT_CODES = new Set([301, 302, 303, 307, 308]);
async function fetchJson(urlStr, token, redirectsLeft = 5) {
    return new Promise((resolve, reject) => {
        const req = https.request(urlStr, {
            headers: buildRequestHeaders(token, { 'Accept': 'application/vnd.github+json' }),
            method: 'GET',
        }, (res) => {
            const status = res.statusCode || 0;
            if (REDIRECT_CODES.has(status)) {
                const loc = res.headers.location;
                if (loc && redirectsLeft > 0) {
                    const nextUrl = new url_1.URL(loc, urlStr).toString();
                    res.resume(); // drain
                    fetchJson(nextUrl, token, redirectsLeft - 1).then(resolve, reject);
                    return;
                }
                reject(new Error(`HTTP ${status}: Redirect with no/too many locations`));
                return;
            }
            if (status < 200 || status >= 300) {
                reject(new Error(`HTTP ${status}: ${res.statusMessage}`));
                return;
            }
            const chunks = [];
            res.on('data', (d) => chunks.push(d));
            res.on('end', () => {
                try {
                    const body = Buffer.concat(chunks).toString('utf8');
                    resolve(JSON.parse(body));
                }
                catch (e) {
                    reject(e);
                }
            });
        });
        req.on('error', reject);
        req.end();
    });
}
async function downloadFile(urlStr, destPath, redirectsLeft = 5) {
    await fs.promises.mkdir(path.dirname(destPath), { recursive: true });
    return new Promise((resolve, reject) => {
        https.get(urlStr, {
            headers: buildRequestHeaders(undefined, { 'Accept': 'application/octet-stream' }),
        }, async (res) => {
            try {
                const status = res.statusCode || 0;
                if (REDIRECT_CODES.has(status)) {
                    const loc = res.headers.location;
                    if (loc && redirectsLeft > 0) {
                        const nextUrl = new url_1.URL(loc, urlStr).toString();
                        res.resume(); // drain
                        try {
                            await downloadFile(nextUrl, destPath, redirectsLeft - 1);
                            resolve();
                        }
                        catch (e) {
                            reject(e);
                        }
                        return;
                    }
                    reject(new Error(`HTTP ${status}: Redirect with no/too many locations`));
                    return;
                }
                if (status < 200 || status >= 300) {
                    reject(new Error(`HTTP ${status}: ${res.statusMessage}`));
                    return;
                }
                const tmpPath = destPath + '.download';
                const file = fs.createWriteStream(tmpPath);
                await streamPipeline(res, file);
                await fs.promises.rename(tmpPath, destPath);
                resolve();
            }
            catch (err) {
                reject(err);
            }
        }).on('error', reject);
    });
}
async function getRelease(repo, tag, token) {
    const base = `https://api.github.com/repos/${repo.owner}/${repo.repo}/releases`;
    const url = tag ? `${base}/tags/${encodeURIComponent(tag)}` : `${base}/latest`;
    return fetchJson(url, token);
}
function pickAsset(info, pattern) {
    const assets = info.assets || [];
    const platform = os.platform();
    const arch = os.arch();
    const preferredPatterns = [];
    if (pattern)
        preferredPatterns.push(pattern);
    // Try to pick reasonable default by platform
    if (platform === 'win32')
        preferredPatterns.push(/win.*(x64|amd64).*\.zip$/i, /windows.*\.zip$/i, /\.zip$/i);
    else if (platform === 'darwin')
        preferredPatterns.push(/mac|darwin.*\.zip$/i, /\.zip$/i, /\.tar\.gz$/i);
    else
        preferredPatterns.push(/linux.*(x64|amd64).*\.zip$/i, /linux.*\.tar\.gz$/i, /\.zip$/i);
    // Arch hints
    if (arch === 'arm64')
        preferredPatterns.unshift(/arm64|aarch64/i);
    for (const pat of preferredPatterns) {
        const found = assets.find(a => pat.test(a.name));
        if (found)
            return { name: found.name, url: found.browser_download_url };
    }
    // Fallback to first zip
    const fallback = assets.find(a => /\.zip$/i.test(a.name));
    if (fallback)
        return { name: fallback.name, url: fallback.browser_download_url };
    return undefined;
}
async function safeExtract(zipPath, destDir) {
    const tmpDir = await fs.promises.mkdtemp(path.join(os.tmpdir(), 'pohlang-extract-'));
    try {
        await extract(zipPath, { dir: tmpDir });
        // Basic validation: ensure directory has something
        const entries = await fs.promises.readdir(tmpDir);
        if (!entries || entries.length === 0)
            throw new Error('Archive appears empty.');
        await fs.promises.mkdir(destDir, { recursive: true });
        // Move extracted content into destDir (replace existing files if any)
        for (const entry of entries) {
            const from = path.join(tmpDir, entry);
            const to = path.join(destDir, entry);
            await fs.promises.rm(to, { recursive: true, force: true });
            await fs.promises.rename(from, to);
        }
    }
    finally {
        // Cleanup
        try {
            await fs.promises.rm(tmpDir, { recursive: true, force: true });
        }
        catch { /* ignore */ }
        try {
            await fs.promises.rm(zipPath, { force: true });
        }
        catch { /* ignore */ }
    }
}
function findBinary(searchDir, names) {
    const entries = fs.readdirSync(searchDir, { withFileTypes: true });
    for (const ent of entries) {
        const full = path.join(searchDir, ent.name);
        if (ent.isDirectory()) {
            const sub = findBinary(full, names);
            if (sub)
                return sub;
        }
        else {
            if (names.includes(ent.name))
                return full;
        }
    }
    return null;
}
async function fetchLatestSDKs(context, opts) {
    const { pohlangRepo, plhubRepo, tagOverride, assetPattern, updateIntervalDays, autoUpdate, githubToken } = getConfig();
    const extensionPath = context.extensionPath;
    const binDir = path.join(extensionPath, 'bin');
    await fs.promises.mkdir(binDir, { recursive: true });
    const versionsPath = path.join(binDir, '.sdk-versions.json');
    let current;
    try {
        const raw = await fs.promises.readFile(versionsPath, 'utf8');
        current = JSON.parse(raw);
    }
    catch { /* no-op */ }
    const now = new Date();
    const needsRefresh = (() => {
        if (opts?.force)
            return true;
        if (!autoUpdate)
            return false;
        if (!current?.fetchedAt)
            return true;
        const last = new Date(current.fetchedAt);
        const ageDays = (now.getTime() - last.getTime()) / (1000 * 60 * 60 * 24);
        return ageDays >= updateIntervalDays;
    })();
    if (!needsRefresh) {
        return current;
    }
    const output = vscode.window.createOutputChannel('PohLang SDK Fetch');
    output.show(true);
    output.appendLine('Fetching latest PohLang and PL-Hub SDKs...');
    // Download PohLang
    const pohlangRel = await getRelease(pohlangRepo, tagOverride, githubToken);
    const pohlangAsset = pickAsset(pohlangRel, assetPattern);
    if (!pohlangAsset)
        throw new Error('Could not find suitable PohLang asset to download.');
    const pohZip = path.join(os.tmpdir(), `pohlang-${Date.now()}.zip`);
    output.appendLine(`Downloading PohLang: ${pohlangRel.tag_name} / ${pohlangAsset.name}`);
    await downloadFile(pohlangAsset.url, pohZip);
    // Extract PohLang into bin/pohlang-dist
    const pohDest = path.join(binDir, 'pohlang-dist');
    await fs.promises.rm(pohDest, { recursive: true, force: true });
    await safeExtract(pohZip, pohDest);
    // Find binary and link/copy to bin/pohlang(.exe)
    const binNames = process.platform === 'win32' ? ['pohlang.exe'] : ['pohlang', 'pohlang.sh'];
    const foundPoh = findBinary(pohDest, binNames);
    if (foundPoh) {
        const targetName = process.platform === 'win32' ? 'pohlang.exe' : 'pohlang';
        const target = path.join(binDir, targetName);
        await fs.promises.rm(target, { force: true });
        await fs.promises.copyFile(foundPoh, target);
        if (process.platform !== 'win32') {
            await fs.promises.chmod(target, 0o755);
        }
    }
    // Download PLHub
    const plhubRel = await getRelease(plhubRepo, tagOverride, githubToken);
    const plhubAsset = pickAsset(plhubRel, assetPattern);
    if (!plhubAsset)
        throw new Error('Could not find suitable PL-Hub asset to download.');
    const plZip = path.join(os.tmpdir(), `plhub-${Date.now()}.zip`);
    output.appendLine(`Downloading PL-Hub: ${plhubRel.tag_name} / ${plhubAsset.name}`);
    await downloadFile(plhubAsset.url, plZip);
    // Extract PLHub into bin/plhub-sdk
    const plDest = path.join(binDir, 'plhub-sdk');
    await fs.promises.rm(plDest, { recursive: true, force: true });
    await safeExtract(plZip, plDest);
    const versions = {
        pohlang: { tag: pohlangRel.tag_name, version: pohlangRel.name || pohlangRel.tag_name, asset: pohlangAsset.name },
        plhub: { tag: plhubRel.tag_name, version: plhubRel.name || plhubRel.tag_name, asset: plhubAsset.name },
        fetchedAt: now.toISOString(),
    };
    await fs.promises.writeFile(versionsPath, JSON.stringify(versions, null, 2), 'utf8');
    output.appendLine('SDKs updated successfully.');
    return versions;
}
exports.fetchLatestSDKs = fetchLatestSDKs;
async function ensureSDKsUpToDate(context, opts) {
    try {
        return await fetchLatestSDKs(context, opts);
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        vscode.window.showWarningMessage(`Failed to update SDKs: ${msg}`);
        return undefined;
    }
}
exports.ensureSDKsUpToDate = ensureSDKsUpToDate;
async function getSDKVersions(context) {
    try {
        const binDir = path.join(context.extensionPath, 'bin');
        const versionsPath = path.join(binDir, '.sdk-versions.json');
        const raw = await fs.promises.readFile(versionsPath, 'utf8');
        return JSON.parse(raw);
    }
    catch {
        return undefined;
    }
}
exports.getSDKVersions = getSDKVersions;
//# sourceMappingURL=fetchLatestSDKs.js.map