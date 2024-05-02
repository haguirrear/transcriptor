import Pristine from "pristinejs";

window.PristineInit = function (form, config, live) {
  const pristine = new Pristine(form, config, live);
  return pristine;
};
