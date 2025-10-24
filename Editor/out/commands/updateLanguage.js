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
exports.updateLanguage = void 0;
const vscode = __importStar(require("vscode"));
const fetchLatestSDKs_1 = require("../utils/fetchLatestSDKs");
async function updateLanguage() {
    const output = vscode.window.createOutputChannel('PohLang Update');
    output.show(true);
    output.appendLine('Updating PohLang interpreter and PL-Hub SDK...');
    try {
        // Use the extension context via the running extension
        const ext = vscode.extensions.getExtension('pohlang.plhub');
        const context = ext?.exports?.context;
        if (!context && ext?.extensionPath) {
            await (0, fetchLatestSDKs_1.fetchLatestSDKs)({ extensionPath: ext.extensionPath }, { force: true });
            vscode.window.showInformationMessage('PohLang and PL-Hub SDKs updated.');
            return;
        }
        if (!context)
            throw new Error('Extension context not available');
        const versions = await (0, fetchLatestSDKs_1.ensureSDKsUpToDate)(context, { force: true });
        if (versions) {
            output.appendLine(`PohLang: ${versions.pohlang?.tag} (${versions.pohlang?.asset})`);
            output.appendLine(`PL-Hub: ${versions.plhub?.tag} (${versions.plhub?.asset})`);
            vscode.window.showInformationMessage('PohLang and PL-Hub SDKs updated successfully.');
        }
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        vscode.window.showErrorMessage(`Update failed: ${msg}`);
        output.appendLine(`Update failed: ${msg}`);
    }
}
exports.updateLanguage = updateLanguage;
//# sourceMappingURL=updateLanguage.js.map

