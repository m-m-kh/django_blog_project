

/*********************/
/*   App Js     */
/*********************/


try {
  // Icon
  lucide.createIcons();
} catch (err) { }



try{
  const toggleButton = document.getElementById('toggleButton');
  const myElement = document.getElementById('nav-links');

  toggleButton.addEventListener('click', function() {
  myElement.classList.toggle('hidden');
  myElement.classList.toggle('block');
  });
}catch (err){}

try {
  class App {

    init() {
  
      const html = document.querySelector("html");
      const toggletheme = document.querySelector("#toggle-theme");
      const lightBtn = toggletheme?.querySelector('.light');
      const darkBtn = toggletheme?.querySelector('.dark');
      toggletheme?.addEventListener('click', () => {
  
        if (html.getAttribute('class') === "dark") {
          document.body.setAttribute("data-layout-mode", "light")
        } else {
          document.body.setAttribute("data-layout-mode", "dark")
        }
  
        html.classList.toggle("dark");
        const isDark = html.classList.contains('dark');
        (!isDark?darkBtn:lightBtn)?.classList.add('hidden');
        (isDark?darkBtn:lightBtn)?.classList.remove('hidden');
  
        // togglethemeicon.className = "ti ti-" + `${themeIcon}` + "  top-icon";
      })
    }
  }
  
  
  
  
  window.addEventListener('DOMContentLoaded', function (e) {
    new App().init();
  })
} catch (err) { }
