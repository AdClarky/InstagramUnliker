# Instagram Unliker

Add config.json file 
```
{
  "firefox_profile_path": "YOUR_PATH_GOES_HERE",
  "liked_posts_path": "liked_posts.json"
}
```


You can download all of your liked posts from Instagram in a data request. Set the output to json, then add to the same directory as this.

Only works with Firefox.
Create a new profile on Firefox, login to Instagram.
Add the path of the profile to the config.

Install requirements

Note before running: there is a 20 second delay between unliking each post. This should hopefuly prevent
Instagram from limiting you.

Run `python unliker.py`
