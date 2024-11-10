
# SEB_Datasience: Room monitoring with Prometheus and Grafana

A brief description of what this project does and who it's for

## Dependencies (On Debian based system)

These dependencies are needed to run the Project. \
Run these commands (from root folder of project) to install the correct dependencies:

### Docker (Newest version with compose plugin)

    for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
    sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" |   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

### Python (Tested and developed on 3.11.2)

    sudo apt install python3 python3-pip

### Python libraries

    pip install -r ./src/requrements.txt

## Environment Variables

To run this project, you will need to check and correct the following environment variables in the enviroment.py file

`DHT_22_PIN`

`AIR_QUALITY_SENSOR_PIN`

`PHOTOSENSOR_PIN`

`PUSHGATEWAY_URL`

Also create a api_key.key file with a openweathermap api key:

`api_key=`

## Deployment

To deploy this project run

    curl -O https://raw.githubusercontent.com/agresdominik/seb_datascience/refs/heads/main/services/setup/setup.sh | bash

## Authors

- [@agresdominik](https://www.github.com/agresdominik)
- [@XanderSEB](https://github.com/XanderSEB)
- [@ErnestPWoz](https://github.com/ErnestPWoz)

## Appendix

Any additional information goes here

## Documentation

[Confluence Internal](https://datasienceseb.atlassian.ne)
