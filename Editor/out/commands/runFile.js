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
exports.runFile = void 0;
const vscode = __importStar(require("vscode"));
const processUtils_1 = require("../utils/processUtils");
const fetchLatestSDKs_1 = require("../utils/fetchLatestSDKs");
const path = __importStar(require("path"));
async function runFile(uri) {
    try {
        // Get the current file URI
        let fileUri;
        if (uri) {
            fileUri = uri;
        }
        else if (vscode.window.activeTextEditor) {
            fileUri = vscode.window.activeTextEditor.document.uri;
        }
        else {
            vscode.window.showErrorMessage('No .poh file is currently open');
            return;
        }
        // Check if it's a .poh file
        if (!fileUri.fsPath.endsWith('.poh')) {
            vscode.window.showErrorMessage('The selected file is not a .poh file');
            return;
        }
        // Ensure SDKs are up to date before running
        const ext = vscode.extensions.getExtension('pohlang.plhub');
        const context = ext?.exports?.context;
        if (context) {
            await (0, fetchLatestSDKs_1.ensureSDKsUpToDate)(context);
        }
        // Show information message
        vscode.window.showInformationMessage(`Running PohLang file: ${path.basename(fileUri.fsPath)}`);
        // Create or show output channel
        const outputChannel = vscode.window.createOutputChannel('PohLang Output');
        outputChannel.show();
        outputChannel.clear();
        outputChannel.appendLine(`Running: ${fileUri.fsPath}`);
        outputChannel.appendLine('---');
        // Run the file using the PohLang interpreter
        const result = await (0, processUtils_1.spawnPohLangProcess)(fileUri.fsPath);
        if (result.success) {
            outputChannel.appendLine(result.stdout);
            if (result.stderr) {
                outputChannel.appendLine('Warnings:');
                outputChannel.appendLine(result.stderr);
            }
            vscode.window.showInformationMessage('PohLang file executed successfully');
        }
        else {
            outputChannel.appendLine('Error executing PohLang file:');
            outputChannel.appendLine(result.stderr || result.stdout);
            vscode.window.showErrorMessage('Failed to execute PohLang file. Check output for details.');
        }
    }
    catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        vscode.window.showErrorMessage(`Error running PohLang file: ${errorMessage}`);
    }
}
exports.runFile = runFile;
//# sourceMappingURL=runFile.js.map