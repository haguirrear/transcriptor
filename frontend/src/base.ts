import Alpine from "alpinejs";
import collapse from "@alpinejs/collapse";
import "htmx.org";
import "./utils/htmx.ts";

window.Alpine = Alpine;
Alpine.plugin(collapse);
Alpine.start();
