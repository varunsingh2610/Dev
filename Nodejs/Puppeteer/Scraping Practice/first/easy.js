const puppeteer = require("puppeteer");
const chalk = require("chalk");

// My OCD of colorful console.logs for debugging..
const error = chalk.bold.red;
const success = chalk.keyword("green");

(async () => {
    try {
        //open the headless browser
        var browser = await puppeteer.launch({ headless: true });
        //open a new page
        var page = await browser.newPage();
        //enter url in page
        await page.goto('https://www.google.com');
        // Google say Cheese!!
        await page.screenshot({ path: "example.png"});
        await browser.close();
        console.log(success("Browser Closed"));
    } catch (err){
        //Catch and display errors
        console.log(error(err));
        await browser.close();
        console.log(error("Browser Closed"));
    }
})();