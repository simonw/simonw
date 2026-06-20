# samesite-lax-demo

Background on my blog: [Exploring the SameSite cookie attribute for preventing CSRF](https://simonwillison.net/2021/Aug/3/samesite/)

This repo holds some tools for exploring the implementation of `SameSite=Lax` (and `SameSite=Strict` and `SameSite=None`) in your browser.

You can set those cookies on this site: https://samesite-lax-demo.vercel.app/

And then use the buttons on https://simonw.github.io/samesite-lax-demo/ - deliberately hosted on an entirely separate domain - to see how they affect navigation to that site using both links and form submissions.

In my explorations using Firefox 89 I get the following:

- For `SameSite=Strict` the cookie I have set is NOT displayed for both link and form navigations
- For `SameSite=None` the cookie I have set is displayed for both link and form navigations
- For `SameSite=Lax` the cookie shows for link navigations but NOT for form navigations
