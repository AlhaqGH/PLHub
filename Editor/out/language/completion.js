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
exports.PohLangCompletionProvider = void 0;
const vscode = __importStar(require("vscode"));
class PohLangCompletionProvider {
    provideCompletionItems(document, position, token, context) {
        const completionItems = [];
        // Get the current line text
        const lineText = document.lineAt(position).text;
        const textBeforeCursor = lineText.substring(0, position.character);
        // Keywords completion
        completionItems.push(...this.getKeywordCompletions());
        // Function-related completions
        if (textBeforeCursor.includes('make') || textBeforeCursor.includes('function')) {
            completionItems.push(...this.getFunctionCompletions());
        }
        // Variable-related completions
        if (textBeforeCursor.includes('set') || textBeforeCursor.includes('variable')) {
            completionItems.push(...this.getVariableCompletions());
        }
        // Control structure completions
        completionItems.push(...this.getControlStructureCompletions());
        // Built-in function completions
        completionItems.push(...this.getBuiltinFunctionCompletions());
        // Operator completions
        completionItems.push(...this.getOperatorCompletions());
        return completionItems;
    }
    getKeywordCompletions() {
        const keywords = [
            { label: 'Start Program', detail: 'Begin program block (v0.5.2)' },
            { label: 'End Program', detail: 'End program block (v0.5.2)' },
            { label: 'Make', detail: 'Create variable or function (v0.5.2)' },
            { label: 'If', detail: 'Conditional statement (v0.5.2)' },
            { label: 'Otherwise', detail: 'Else clause (v0.5.2)' },
            { label: 'End If', detail: 'End If block (v0.5.2)' },
            { label: 'While', detail: 'While loop (v0.5.2)' },
            { label: 'End While', detail: 'End While block (v0.5.2)' },
            { label: 'Repeat', detail: 'Repeat N times loop (v0.5.2)' },
            { label: 'Break', detail: 'Break out of a loop' },
            { label: 'Continue', detail: 'Continue to next loop iteration' },
            { label: 'Use', detail: 'Use module or library' },
            { label: 'Import', detail: 'Import module' },
            { label: 'Increase', detail: 'Increment variable by value' },
            { label: 'Decrease', detail: 'Decrement variable by value' },
            { label: 'Ask for', detail: 'Get user input (v0.5.2)' },
            { label: 'Write', detail: 'Output text (v0.5.2)' },
            { label: 'true', detail: 'Boolean true value' },
            { label: 'false', detail: 'Boolean false value' },
            { label: 'null', detail: 'Null value' },
            { label: 'and', detail: 'Logical AND operator' },
            { label: 'or', detail: 'Logical OR operator' },
            { label: 'not', detail: 'Logical NOT operator' }
        ];
        return keywords.map(keyword => {
            const item = new vscode.CompletionItem(keyword.label, vscode.CompletionItemKind.Keyword);
            item.detail = keyword.detail;
            return item;
        });
    }
    getFunctionCompletions() {
        const functionCompletion = new vscode.CompletionItem('Make function', vscode.CompletionItemKind.Snippet);
        functionCompletion.insertText = new vscode.SnippetString('Make ${1:name} with ${2:param1}:\n\t${3:# function body}\nEnd');
        functionCompletion.detail = 'Create a new function (v0.5.2)';
        functionCompletion.documentation = 'Creates a new function with parameters';
        const functionNoParams = new vscode.CompletionItem('Make function (no params)', vscode.CompletionItemKind.Snippet);
        functionNoParams.insertText = new vscode.SnippetString('Make ${1:name}:\n\t${2:# function body}\nEnd');
        functionNoParams.detail = 'Create function without parameters (v0.5.2)';
        functionNoParams.documentation = 'Creates a new function without parameters';
        return [functionCompletion, functionNoParams];
    }
    getVariableCompletions() {
        const makeCompletion = new vscode.CompletionItem('Make variable', vscode.CompletionItemKind.Snippet);
        makeCompletion.insertText = new vscode.SnippetString('Make ${1:name} = ${2:value}');
        makeCompletion.detail = 'Create a new variable (v0.5.2)';
        return [makeCompletion];
    }
    getControlStructureCompletions() {
        const ifCompletion = new vscode.CompletionItem('If', vscode.CompletionItemKind.Snippet);
        ifCompletion.insertText = new vscode.SnippetString('If ${1:condition}:\n\t${2:# code}\nEnd If');
        ifCompletion.detail = 'If statement (v0.5.2)';
        const ifElseCompletion = new vscode.CompletionItem('If Otherwise', vscode.CompletionItemKind.Snippet);
        ifElseCompletion.insertText = new vscode.SnippetString('If ${1:condition}:\n\t${2:# if code}\nOtherwise:\n\t${3:# else code}\nEnd If');
        ifElseCompletion.detail = 'If-Otherwise statement (v0.5.2)';
        const whileCompletion = new vscode.CompletionItem('While', vscode.CompletionItemKind.Snippet);
        whileCompletion.insertText = new vscode.SnippetString('While ${1:condition}:\n\t${2:# loop body}\nEnd While');
        whileCompletion.detail = 'While loop (v0.5.2)';
        const repeatCompletion = new vscode.CompletionItem('Repeat', vscode.CompletionItemKind.Snippet);
        repeatCompletion.insertText = new vscode.SnippetString('Repeat ${1:times}:\n\t${2:# loop body}\nEnd');
        repeatCompletion.detail = 'Repeat loop (v0.5.2)';
        return [ifCompletion, ifElseCompletion, whileCompletion, repeatCompletion];
    }
    getBuiltinFunctionCompletions() {
        const builtins = [
            // Core I/O (v0.5.2)
            {
                label: 'Write',
                insertText: 'Write "${1:message}"',
                detail: 'Write output to console (v0.5.2)'
            },
            {
                label: 'Ask for',
                insertText: 'Ask for "${1:prompt}"',
                detail: 'Get user input (v0.5.2)'
            },
            {
                label: 'Import',
                insertText: 'Import "${1:module}"',
                detail: 'Import a module (v0.5.2)'
            },
            // Math phrasal expressions
            {
                label: 'total of',
                insertText: 'total of ${1:list}',
                detail: 'Sum all elements in a list'
            },
            {
                label: 'smallest in',
                insertText: 'smallest in ${1:list}',
                detail: 'Find minimum value'
            },
            {
                label: 'largest in',
                insertText: 'largest in ${1:list}',
                detail: 'Find maximum value'
            },
            {
                label: 'absolute value of',
                insertText: 'absolute value of ${1:number}',
                detail: 'Get absolute value'
            },
            {
                label: 'round',
                insertText: 'round ${1:number}',
                detail: 'Round to nearest integer'
            },
            {
                label: 'round down',
                insertText: 'round down ${1:number}',
                detail: 'Round down (floor)'
            },
            {
                label: 'round up',
                insertText: 'round up ${1:number}',
                detail: 'Round up (ceiling)'
            },
            // String phrasal expressions
            {
                label: 'make uppercase',
                insertText: 'make uppercase ${1:text}',
                detail: 'Convert to uppercase'
            },
            {
                label: 'make lowercase',
                insertText: 'make lowercase ${1:text}',
                detail: 'Convert to lowercase'
            },
            {
                label: 'trim spaces from',
                insertText: 'trim spaces from ${1:text}',
                detail: 'Remove leading/trailing spaces'
            },
            // Collection phrasal expressions
            {
                label: 'first in',
                insertText: 'first in ${1:list}',
                detail: 'Get first element'
            },
            {
                label: 'last in',
                insertText: 'last in ${1:list}',
                detail: 'Get last element'
            },
            {
                label: 'reverse of',
                insertText: 'reverse of ${1:list}',
                detail: 'Reverse a list'
            },
            {
                label: 'count of',
                insertText: 'count of ${1:list}',
                detail: 'Get number of elements'
            },
            {
                label: 'join...with',
                insertText: 'join ${1:list} with "${2:,}"',
                detail: 'Join list with separator'
            },
            {
                label: 'split...by',
                insertText: 'split ${1:text} by "${2:,}"',
                detail: 'Split string by delimiter'
            },
            {
                label: 'contains...in',
                insertText: 'contains ${1:item} in ${2:list}',
                detail: 'Check if item is in list'
            },
            {
                label: 'remove...from',
                insertText: 'remove ${1:item} from ${2:list}',
                detail: 'Remove item from list'
            },
            {
                label: 'append...to',
                insertText: 'append ${1:item} to ${2:list}',
                detail: 'Add item to end of list'
            },
            {
                label: 'insert...at',
                insertText: 'insert ${1:item} at ${2:index}',
                detail: 'Insert item at specific position'
            }
        ];
        return builtins.map(builtin => {
            const item = new vscode.CompletionItem(builtin.label, vscode.CompletionItemKind.Function);
            item.insertText = new vscode.SnippetString(builtin.insertText);
            item.detail = builtin.detail;
            return item;
        });
    }
    getOperatorCompletions() {
        const operators = [
            // Phrasal operators
            {
                label: 'plus',
                insertText: '${1:a} plus ${2:b}',
                detail: 'Addition (phrasal)'
            },
            {
                label: 'minus',
                insertText: '${1:a} minus ${2:b}',
                detail: 'Subtraction (phrasal)'
            },
            {
                label: 'times',
                insertText: '${1:a} times ${2:b}',
                detail: 'Multiplication (phrasal)'
            },
            {
                label: 'divided by',
                insertText: '${1:a} divided by ${2:b}',
                detail: 'Division (phrasal)'
            },
            {
                label: 'is equal to',
                insertText: '${1:a} is equal to ${2:b}',
                detail: 'Equality comparison (phrasal)'
            },
            {
                label: 'is greater than',
                insertText: '${1:a} is greater than ${2:b}',
                detail: 'Greater than comparison (phrasal)'
            },
            {
                label: 'is less than',
                insertText: '${1:a} is less than ${2:b}',
                detail: 'Less than comparison (phrasal)'
            },
            // Symbolic operators (v0.5.2)
            {
                label: '+',
                insertText: '${1:a} + ${2:b}',
                detail: 'Addition (symbolic)'
            },
            {
                label: '-',
                insertText: '${1:a} - ${2:b}',
                detail: 'Subtraction (symbolic)'
            },
            {
                label: '*',
                insertText: '${1:a} * ${2:b}',
                detail: 'Multiplication (symbolic)'
            },
            {
                label: '/',
                insertText: '${1:a} / ${2:b}',
                detail: 'Division (symbolic)'
            },
            {
                label: '==',
                insertText: '${1:a} == ${2:b}',
                detail: 'Equality (symbolic)'
            },
            {
                label: '!=',
                insertText: '${1:a} != ${2:b}',
                detail: 'Not equal (symbolic)'
            },
            {
                label: '<',
                insertText: '${1:a} < ${2:b}',
                detail: 'Less than (symbolic)'
            },
            {
                label: '>',
                insertText: '${1:a} > ${2:b}',
                detail: 'Greater than (symbolic)'
            },
            {
                label: '<=',
                insertText: '${1:a} <= ${2:b}',
                detail: 'Less or equal (symbolic)'
            },
            {
                label: '>=',
                insertText: '${1:a} >= ${2:b}',
                detail: 'Greater or equal (symbolic)'
            }
        ];
        return operators.map(operator => {
            const item = new vscode.CompletionItem(operator.label, vscode.CompletionItemKind.Operator);
            item.insertText = new vscode.SnippetString(operator.insertText);
            item.detail = operator.detail;
            return item;
        });
    }
}
exports.PohLangCompletionProvider = PohLangCompletionProvider;
//# sourceMappingURL=completion.js.map