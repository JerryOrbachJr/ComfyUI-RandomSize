import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

function displayMessage(message) {
	var w = this.widgets?.find((w) => w.name === "display_text_widget");
	if (w === undefined) {
		w = ComfyWidgets["STRING"](this, "display_text_widget", ["STRING", { multiline: true }], app).widget;
		w.inputEl.readOnly = true;
		w.inputEl.style.opacity = 0.6;
		w.inputEl.style.fontSize = "9pt";
	}
    const display = message.join('\n');
	w.value = 'Sizes in present:\n' + display;
	this.onResize?.(this.size);
};

const ext = {
	name: "jojr.random-sizes.displaymessage",
    async setup() {
        function messageHandler(event) {
            const id = event.detail.id;
            const message = event.detail.message;
            const node = app.graph._nodes_by_id[id];
            if (node && node.displayMessage) node.displayMessage(message);
            else (console.log(`node ${id} couldn't handle a message`));
        }
        api.addEventListener("jojr.random-sizes.sendmessage", messageHandler);
    },
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeType.comfyClass=="JOJR_RandomSize" ) {
            nodeType.prototype.displayMessage = displayMessage;
        }
    }
}

app.registerExtension(ext)