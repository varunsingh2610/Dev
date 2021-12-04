const puppeteer = require("puppeteer");
const chalk = require("chalk");

(async () => {
    const browser = await puppeteer.launch({headless: false});
    const page = await browser.newPage();
   
    // set the viewport so we know the dimensions of the screen
    await page.setViewport({ width: 800, height: 600 });
   
    // go to a page setup for mouse event tracking
    await page.goto('https://github.com/login');
   
    // click an area
    // await page.mouse.click('[name="commit"]');
    const elements = await page.$x('//*[@id="login"]/div[4]/form/div/input[12]')
    await elements[0].click() 

    // await page.mouse.click(132, 103, { button: 'left' });
   
    // the screenshot should show feedback from the page that right part was clicked.
    await page.screenshot({ path: 'mouse_click.png' });
    // await browser.close();
   })()