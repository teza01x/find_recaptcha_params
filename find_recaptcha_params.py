import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


if __name__ == "__main__":
    options = Options()
    your_googlEXE_path = "" # put here path to your google.exe file
    options.binary_location = your_googlEXE_path
    # put in current folder chromedriver.exe with your compatible version of google.exe
    browser = Chrome("chromedriver.exe", chrome_options=options)
    browser.maximize_window()
    url = '' # put here url of page where u need to solve reCAPTCHA
    browser.get(url)
    time.sleep(10)


    js_code = """
    function findRecaptchaClients() {
      if (typeof (___grecaptcha_cfg) !== 'undefined') {
        return Object.entries(___grecaptcha_cfg.clients).map(([cid, client]) => {
          const data = { id: cid, version: cid >= 10000 ? 'V3' : 'V2' };
          const objects = Object.entries(client).filter(([_, value]) => value && typeof value === 'object');

          objects.forEach(([toplevelKey, toplevel]) => {
            const found = Object.entries(toplevel).find(([_, value]) => (
              value && typeof value === 'object' && 'sitekey' in value && 'size' in value
            ));

            if (typeof toplevel === 'object' && toplevel instanceof HTMLElement && toplevel['tagName'] === 'DIV'){
                data.pageurl = toplevel.baseURI;
            }

            if (found) {
              const [sublevelKey, sublevel] = found;

              data.sitekey = sublevel.sitekey;
              const callbackKey = data.version === 'V2' ? 'callback' : 'promise-callback';
              const callback = sublevel[callbackKey];
              if (!callback) {
                data.callback = null;
                data.function = null;
              } else {
                data.function = callback;
                const keys = [cid, toplevelKey, sublevelKey, callbackKey].map((key) => `['${key}']`).join('');
                data.callback = `___grecaptcha_cfg.clients${keys}`;
              }
            }
          });
          return data;
        });
      }
      return [];
    }

    return findRecaptchaClients();
    """

    result = browser.execute_script(js_code)
    print(result)

