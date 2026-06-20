#  Prompts

[![npm version](https://img.shields.io/npm/v/prompts-js)](https://www.npmjs.com/package/prompts-js)
[![License: Apache2](https://img.shields.io/badge/License-Apache2-blue.svg)](https://opensource.org/license/apache-2-0)

A lightweight, dependency-free JavaScript library for creating accessible modal alert, confirm, and prompt dialogs. This library implements an async promise-based approach as an alternative to the browser built-in `alert()`, `confirm()`, and `prompt()` functions.

## Features

*   **Keyboard accessible:**  Built with keyboard navigation in mind, including focus trapping and keyboard navigation (Tab, Shift+Tab, Escape, Enter).
*   **Promise-based:**  Uses Promises to allow for easy async/await usage.
*   **No Dependencies:**  Written in pure JavaScript, requiring no external libraries or frameworks.
*   **Lightweight:**  The library is small and designed to add minimal overhead to your project.

## Installation

```bash
npm install prompts-js
```
Or use it from a CDN:
```html
<script src="https://cdn.jsdelivr.net/npm/prompts-js"></script>
```

## Usage

```javascript
// Alert
await Prompts.alert("This is an alert message!");
console.log("Alert closed");

// Confirm
const confirmed = await Prompts.confirm("Are you sure you want to proceed?");
if (confirmed) {
  console.log("User confirmed");
} else {
  console.log("User canceled");
}

// Prompt for a string
const userInput = await Prompts.prompt("Please enter your name:");
if (userInput) {
  console.log("User entered:", userInput);
} else {
  console.log("User canceled or entered nothing");
}
```

## API

### `await Prompts.alert(message)`

Displays an alert dialog with an "OK" button.

*   `message` (string): The message to display in the alert.

### `await Prompts.confirm(message)`

Displays a confirmation dialog with "OK" and "Cancel" buttons.

*   `message` (string): The message to display in the confirmation dialog.
*   Resolves: `true` if the user clicks "OK", `false` if they click "Cancel" or press escape.

### `await Prompts.prompt(message)`

Displays a prompt dialog with a text input field and "OK" and "Cancel" buttons.

*   `message` (string): The message to display above the input field.
*   Resolves: the user's input (string) if they click "OK", `null` if they click "Cancel" or press escape.
