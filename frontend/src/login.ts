import Pristine from "pristinejs";

document.addEventListener("alpine:init", () => {
  Alpine.data("loginData", () => ({
    loading: false,
    pristine: undefined,
    formInit() {
      this.pristine = new Pristine(this.$refs.form, {
        errorClass: "border-red-500",
        errorTextClass: "text-red-500 pt-2",
      });
    },
    handleValidation(event) {
      const valid = this.pristine.validate();
      console.log("Form valid:", valid);
      if (!valid) {
        event.preventDefault();
      } else {
        this.loading = true;
      }
    },
    inputHandler() {
      this.$refs.backendError.innerText = "";
    },
  }));
});
