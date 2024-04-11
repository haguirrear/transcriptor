import Pristine from "pristinejs";

window["Pristine"] = function (form, config, live) {
  const pristine = new Pristine(form, config, live);
  return pristine;
};
