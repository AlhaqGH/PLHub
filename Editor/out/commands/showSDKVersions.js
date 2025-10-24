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
exports.showSDKVersions = void 0;
const vscode = __importStar(require("vscode"));
const fetchLatestSDKs_1 = require("../utils/fetchLatestSDKs");
async function showSDKVersions() {
    // Try to get extension context to ensure SDKs file location
    const ext = vscode.extensions.getExtension('pohlang.plhub');
    const context = ext?.exports?.context;
    try {
        // Optionally refresh versions if none exist yet
        let versions = context ? await (0, fetchLatestSDKs_1.getSDKVersions)(context) : undefined;
        if (!versions && context) {
            await (0, fetchLatestSDKs_1.ensureSDKsUpToDate)(context);
            versions = await (0, fetchLatestSDKs_1.getSDKVersions)(context);
        }
        if (!versions) {
            vscode.window.showInformationMessage('No SDK versions found yet. Run "PL-Hub: Update Language" to fetch the SDKs.');
            return;
        }
        const lines = [];
        if (versions.pohlang) {
            lines.push(`PohLang: ${versions.pohlang.version} (${versions.pohlang.tag}) - ${versions.pohlang.asset ?? ''}`.trim());
        }
        else {
            lines.push('PohLang: not installed');
        }
        if (versions.plhub) {
            lines.push(`PL-Hub: ${versions.plhub.version} (${versions.plhub.tag}) - ${versions.plhub.asset ?? ''}`.trim());
        }
        else {
            lines.push('PL-Hub: not installed');
        }
        lines.push(`Fetched: ${versions.fetchedAt}`);
        const message = lines.join('\n');
        const output = vscode.window.createOutputChannel('PohLang SDK Versions');
        output.clear();
        output.appendLine(message);
        output.show(true);
        vscode.window.showInformationMessage('Displayed current PohLang/PL-Hub SDK versions in Output.');
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        vscode.window.showErrorMessage(`Failed to read SDK versions: ${msg}`);
    }
}
exports.showSDKVersions = showSDKVersions;
//# sourceMappingURL=showSDKVersions.js.map

