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
            const originalNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = async function () {
              if (originalNodeCreated) {
                originalNodeCreated.apply(this, arguments);
              }

              const presetWidget = this.widgets.find((w) => w.name === "preset");
              const sizeIndexWidget = this.widgets.find((w) => w.name === "seed");

              const fetchSizes = async (preset) => {
                try {
                  const response = await fetch("/JOJR_RandomSize/get_sizes", {
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                      preset: preset,
                    }),
                  });

                  if (response.ok) {
                    const sizes = await response.json();
                    console.log("Fetched sizes:", sizes);
                    return sizes;
                  } else {
                    console.error(`Failed to fetch sizes: ${response.status}`);
                    return [];
                  }
                } catch (error) {
                  console.error(`Error fetching sizes for preset ${preset}:`, error);
                  return [];
                }
              };

              const updateSizeIndex = async () => {
                const preset = presetWidget.value;

                console.log(`Selected preset: ${preset}`);

                const sizes = await fetchSizes(preset);

                if (!sizes || !sizes.length) return;

                sizeIndexWidget.options.max = sizes.length;
                if(sizeIndexWidget.options.value > sizes.length) {
                    sizeIndexWidget.options.value = sizes.length;
                }

                this.triggerSlot(0);
              };

              presetWidget.callback = updateSizeIndex;

              // Initial update
              await updateSizeIndex();
            };
        }
    }
}

app.registerExtension(ext)