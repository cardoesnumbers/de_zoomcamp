
Finally got to Kestras login page. The main issue preventing this was localhost:8080 is not compatible with they way Github Codespaces work. Basically:

- The Docker container is running inside a remote VM
- You need to use the forwarded port URL, not localhost. 
- The login URL is the name of my codespaces + a bunch of numbers + .app.github.dev/ui/login?from=/dashboards
- The actual URL could have been checked earlier looking at the PORTS menu :)
- I guess the intention was to run this locally?

I also had the original docker compose file in the same folder, even with a different name (but same extension) it seemsd to be causing some confusion when running the docker compose up command. At the end I changed the extension to .bak 