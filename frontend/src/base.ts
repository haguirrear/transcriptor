import Alpine from "alpinejs";
import collapse from "@alpinejs/collapse";
import morph from "@alpinejs/morph";
import "htmx.org";
import "./utils/htmx.ts";
import "htmx-ext-loading-states";

window.Alpine = Alpine;
Alpine.plugin(collapse);
Alpine.plugin(morph);
Alpine.start();

htmx.logger = function (elt, event, data) {
  if (console) {
    console.log(event, elt, data);
  }
};
