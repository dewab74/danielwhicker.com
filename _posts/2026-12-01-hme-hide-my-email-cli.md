---
layout: post
date: 2026-12-01 09:00:00 -0600
title: "hme: iCloud Hide My Email from the terminal"
description: "A single-binary CLI for iCloud+ Hide My Email. Make an address, have it on the clipboard, move on."
accent: automation
tags: [cli, privacy, icloud]
---

I like Hide My Email. A fresh throwaway address for every sign-up means a leaked
one is a problem I can switch off.

I don't like making them. That's a detour through Settings or icloud.com, and
1Password has no Hide My Email integration, so it can't create one when I sign up
somewhere.

So I wrote **hme**. I wanted these addresses from a terminal, on my own machines,
without clicking through Settings. Yes, it's a command line tool for something with
a perfectly good website.

{% include get-it.html id="hme" %}

## If I'd used Fastmail, I wouldn't need this

1Password has a
[Fastmail integration](https://support.1password.com/fastmail/). On a sign-up
page you click the email field, pick Create Masked Email, and 1Password fills in a
fresh alias. You can block it later from the same login. That's exactly what I
wanted from iCloud.

I self-hosted my own mail for 30 years, and I had a fully bespoke way of making
masked addresses for it. Then I decided to let Apple deal with that particular
headache, mostly because it's included in my iCloud plan and doesn't cost me
anything extra. Yay! No more AWS bill! The catch is that iCloud has no 1Password
integration, hence hme.

## Getting it

On macOS or Linux, Homebrew is the easy way:

```bash
brew tap dewab-org/custom && { brew trust --formula dewab-org/custom/hme 2>/dev/null || true; } && brew install dewab-org/custom/hme
```

The `brew trust` step is for Homebrew 7 and newer. Older versions skip it.

Or grab an archive from the release page and check it against `checksums.txt`. It's
one static binary for macOS, Linux and Windows, on amd64 and arm64.

## Using it

```bash
hme login                          # Apple ID, password, 2FA code; once
hme generate -d "Acme store"       # new address, copied to the clipboard
hme list --active                  # what's in use
hme deactivate example-alias.4x@icloud.com
hme delete example-alias.4x@icloud.com
```

It signs in to iCloud itself, so there's no browser, no cookie export and no other
runtime. It can also relabel and pause addresses and change where they forward.

A whole session, against a simulated account, so every address is invented:

<figure>
<img src="{{ '/assets/img/hme/demo.gif' | relative_url }}"
  width="1084" height="483"
  alt="A terminal recording of a full hme session: signing in through 1Password, making two
  addresses, listing them, copying one, deleting an old one and listing what is left.">
</figure>

The second `generate` also saves a login in 1Password, which is the gap I started
with. `copy` matches loosely, and `delete` only matches exactly and asks first.

<details class="recording" markdown="1">
<summary>The commands, as text</summary>

```text
$ hme login --1password "Apple ID"
Apple sent a verification code to your trusted devices.
Verification code: 123456
Signed in as tester@example.com.
$ hme generate -d "Acme store"
plover-tidbit.4x@icloud.com
Copied to the clipboard.
$ hme generate -d "Acme forum" --1password --url acme.example
amber-sprocket.2q@icloud.com
Copied to the clipboard.
Saved a login for https://acme.example to 1Password as "Acme forum" in the Private vault, with a generated password.
$ hme list
ADDRESS                       LABEL             STATUS    CREATED     NOTE
amber-sprocket.2q@icloud.com  Acme forum        active    2026-11-19
plover-tidbit.4x@icloud.com   Acme store        active    2026-11-19
quiet-meadow.4k@icloud.com    Grocery delivery  active    2026-11-16
copper-kettle.8r@icloud.com   Newsletter        active    2026-10-10  weekly digest
nimble-ferry.1z@icloud.com    Airline loyalty   active    2026-08-16
dusty-almanac.5p@icloud.com   Old forum         inactive  2025-10-15  spam after breach
$ hme copy grocery
quiet-meadow.4k@icloud.com
Copied to the clipboard.
$ hme delete dusty-almanac.5p@icloud.com
This permanently deletes:
  dusty-almanac.5p@icloud.com  Old forum
Delete? [y/N] y
Deleted dusty-almanac.5p@icloud.com.
$ hme list --inactive
No addresses match.
```

</details>

It's scriptable too. Results go to stdout and chatter to stderr, every command
takes `--json` with a stable shape, and there are distinct exit codes for "you used
it wrong" and "sign in again".

## What about my password?

A session that can manage your iCloud addresses is nearly as good as the password,
so hme treats it that way.

- The session is **encrypted on disk**, with the key in the OS credential store
  (Keychain on macOS). With no store, it falls back to an owner-only file and says so.
- It **only talks to Apple.** Addresses and cookies are checked against Apple
  domains, HTTPS is required, and redirects aren't followed.
- **Deletes ask first.** With no terminal and no `--yes`, it refuses.

## The honest bit

hme is early days. That said:

- There's an extensive test suite, run against a protocol-faithful fake of Apple's
  services.
- Sign-in and every command have been checked once against a real account on macOS.
- It hasn't been exercised on Linux or Windows beyond the test suite.
- Nobody independent has reviewed the sign-in and cryptography code.
- Apple publishes no API for Hide My Email, so this can break whenever Apple
  changes something.

I wrote it for myself and shared it in case it's useful. Read the code before you
trust it with your Apple Account, and expect to report a bug or two. If 1Password
ever adds Hide My Email itself, hme probably isn't needed anymore.

You'll need iCloud+, with **Access iCloud Data on the Web** turned on. That setting
is off when Advanced Data Protection is on.
