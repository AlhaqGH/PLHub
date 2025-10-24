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
exports.runEnvironmentExample = void 0;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const cp = __importStar(require("child_process"));
const fetchLatestSDKs_1 = require("../utils/fetchLatestSDKs");
async function runEnvironmentExample() {
    const output = vscode.window.createOutputChannel('PohLang Example');
    output.show(true);
    try {
        const ext = vscode.extensions.getExtension('pohlang.plhub');
        const context = ext?.exports?.context;
        if (!context)
            throw new Error('Extension context not available');
        await (0, fetchLatestSDKs_1.ensureSDKsUpToDate)(context);
        const binDir = path.join(context.extensionPath, 'bin');
        const pohlangBin = path.join(binDir, process.platform === 'win32' ? 'pohlang.exe' : 'pohlang');
        // Create a sample script under the workspace or bin
        const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        const scriptPath = path.join(workspace ?? binDir, 'example.poh');
        const content = Buffer.from('print "PohLang Environment OK"\n', 'utf8');
        await vscode.workspace.fs.writeFile(vscode.Uri.file(scriptPath), content);
        const proc = cp.spawn(pohlangBin, [scriptPath], { shell: process.platform === 'win32' });
        proc.stdout.on('data', d => output.append(d.toString()));
        proc.stderr.on('data', d => output.append(d.toString()));
        proc.on('close', code => {
            output.appendLine(`\nProcess exited with code ${code}`);
            if (code === 0) {
                vscode.window.showInformationMessage('Environment example ran successfully.');
            }
            else {
                vscode.window.showErrorMessage('Environment example failed. Check output for details.');
            }
        });
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        vscode.window.showErrorMessage(`Failed to run example: ${msg}`);
        output.appendLine(`Failed to run example: ${msg}`);
    }
}
exports.runEnvironmentExample = runEnvironmentExample;
//# sourceMappingURL=runEnvironmentExample.js.map

