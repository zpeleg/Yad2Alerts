# Goals
1. Notify me whenever a new listing goes up
    1. Parse the page completely
        1. ~~Download page~~
        3. ~~Create good data structure for ad~~
        3. ~~Parse into structure~~
        4. ~~Add __repr__~~
    2. Parse multi pages
        1. ~~Parse urls in page~~
        2. ~~Extract to objects~~
        3. ~~Download rest of urls~~
        4. Do that recursively to get all pages
        5. Collate all car ad objects to one
    3. ~~Change to selenium because requests isn't working~~
    3. Test whether car salesmen appear and classify them as such
    3. Find unique id for ads
    4. Store them in db
    5. Compare with previous stuff in db and show when new ad is up
    6. Notify with telegram
    7. Upload to amazon
2. Create api from that
3. Create website from api