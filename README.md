# Mom, can we have Pretendo at home?

Yes, son.

## About this project

This is my **work-in-progress** amateur attempt at creating a development environment for Pretendo Network. It can be thought of as a spiritual successor to the outdated and now archived [pretendo-docker](https://github.com/MatthewL246/pretendo-docker) project, with the aim to run modern Pretendo servers. For example, [Opaque tokens](https://pretendo.network/blog/7-17-26) are one thing that's missing in pretendo-docker.

I have decided to divert from the former in the following ways:

- Use official images only: Instead of building all repos locally, this setup will pull in official Docker images from Pretendo. (To replace a pod for testing purposes, you will need to clone it yourself; `override.Dockerfile` and `override/` are gitignored for this purpose.)

- Split the compose setup: Each pod has its own compose.yml file. Compose files are then included by the compose.yml file in the root of the repository, which is what gets run.

- Minimize the use of shell scripts: The only shell script in this project is what builds the aforementioned main compose file. Server maintenance (creation of databases, S3 buckets, etc...) is managed by Ansible. This reduces the dependency on Linux/WSL and simplifies maintenance (and I just dislike shell scripts in general lol)

- Only use a single .env file in the root of the repository. "Constant" environment variables (those that need to be set but aren't necessarily secret) are declared in the compose.yml files, and the required variables get interpolated by Docker at parse time. This means that Docker will refuse to run if any variable is missing, but I see this as a benefit; if something is missing, you see it right away instead of having to debug weird behaviour for hours.

## How to set this up?

I'm still working out the kinks (only the friends list and accounts server work for now), so right now, if you want to try this, you'll be on your own. If you run into anything or want to help, shoot me a message on Discord or send an email.