to setup environment:
1. to reset docker environment (and making sure we are starting from scratch):
    1.a. make sure no active containers are running by typing sudo docker ps
        1.a.a. if there is an active container, type sudo docker stop <container_name>
    1.b. sudo docker system prune -a
2. build the spreader ecosystem by running: ./setupEnvironment/build_spreader_ecosystem.sh
    2.a - if there is a problem running bash scripts, type dos2unix <filename> and then rerun the script
3. start the spreader ecosystem by running ./setupEnvironment/build_spreader_ecosystem.sh