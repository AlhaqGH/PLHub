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
exports.deactivate = exports.activate = exports.extensionContext = void 0;
const vscode = __importStar(require("vscode"));
const runFile_1 = require("./commands/runFile");
const createProject_1 = require("./commands/createProject");
const updateLanguage_1 = require("./commands/updateLanguage");
const diagnostics_1 = require("./language/diagnostics");
const completion_1 = require("./language/completion");
const runEnvironmentExample_1 = require("./commands/runEnvironmentExample");
const showSDKVersions_1 = require("./commands/showSDKVersions");
let diagnostics;
function activate(context) {
    exports.extensionContext = context;
    console.log('PohLang Hub extension is now active!');
    // Initialize diagnostics provider
    diagnostics = new diagnostics_1.PohLangDiagnostics(context);
    // Register completion provider
    const completionProvider = vscode.languages.registerCompletionItemProvider('pohlang', new completion_1.PohLangCompletionProvider(), '.', ' ');
    // Register commands
    const runFileCommand = vscode.commands.registerCommand('PLHub.runFile', (uri) => {
        (0, runFile_1.runFile)(uri);
    });
    const createProjectCommand = vscode.commands.registerCommand('PLHub.createProject', () => {
        (0, createProject_1.createProject)();
    });
    const updateLanguageCommand = vscode.commands.registerCommand('PLHub.updateLanguage', () => {
        (0, updateLanguage_1.updateLanguage)();
    });
    const runEnvExampleCommand = vscode.commands.registerCommand('PLHub.runEnvironmentExample', () => {
        (0, runEnvironmentExample_1.runEnvironmentExample)();
    });
    const showSDKVersionsCommand = vscode.commands.registerCommand('PLHub.showSDKVersions', () => {
        (0, showSDKVersions_1.showSDKVersions)();
    });
    // Add to subscriptions
    context.subscriptions.push(runFileCommand, createProjectCommand, updateLanguageCommand, runEnvExampleCommand, showSDKVersionsCommand, completionProvider, diagnostics);
    // Register file change listener for .poh files
    const fileWatcher = vscode.workspace.createFileSystemWatcher('**/*.poh');
    fileWatcher.onDidChange((uri) => {
        diagnostics.updateDiagnostics(uri);
    });
    fileWatcher.onDidCreate((uri) => {
        diagnostics.updateDiagnostics(uri);
    });
    context.subscriptions.push(fileWatcher);
    // Show activation message
    vscode.window.showInformationMessage('PohLang Hub extension activated! Ready to work with .poh files.');
    // Expose context for internal utilities that need extensionPath
    return { context };
}
exports.activate = activate;
function deactivate() {
    console.log('PohLang Hub extension is deactivated');
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map