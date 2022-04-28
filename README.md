1) You must create env.toml from env-sample.toml 
2) docker build -t CrossPosterBot . 
3) docker run --network=host --restart=unless-stopped -d CrossPosterBot
