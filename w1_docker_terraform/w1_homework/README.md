#Week 1 Homework


Question 1. Understanding Docker images. Answer: pip version 25.3

Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.

I need a docker container of python 3.13 (in this case using the relevant Debian version), use bash as entrypoint, interactive. What I need to do:
- Pull the image
- command RUN + -it (interactive terminal) + setting the entrypoint + [docker image] (from Video)
- interact with it :)

@cardoesnumbers ➜ /workspaces/de_zoomcamp/w1_docker_terraform/pipeline (main) $ docker --version
Docker version 28.5.1-1, build e180ab8ab82d22b7895a3e6e110cf6dd5c45f1d7
@cardoesnumbers ➜ /workspaces/de_zoomcamp/w1_docker_terraform/pipeline (main) $ docker pull python:3.13
3.13: Pulling from library/python
Digest: sha256:c8b03b4e98b39cfb180a5ea13ae5ee39039a8f75ccf52fe6d5c216eed6e1be1d
Status: Image is up to date for python:3.13
docker.io/library/python:3.13
@cardoesnumbers ➜ /workspaces/de_zoomcamp/w1_docker_terraform/pipeline (main) $ docker run -it --entrypoint bash python:3.13
root@7ac1463f2370:/# pip --version
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)

Trying other python versions:

@cardoesnumbers ➜ /workspaces/de_zoomcamp/w1_docker_terraform/w1_homework (main) $ docker --version
Docker version 28.5.1-1, build e180ab8ab82d22b7895a3e6e110cf6dd5c45f1d7
@cardoesnumbers ➜ /workspaces/de_zoomcamp/w1_docker_terraform/w1_homework (main) $ docker pull python:3.13-slim-bookworm
3.13-slim-bookworm: Pulling from library/python
c02d17997ce3: Pull complete 
147314ac1e23: Pull complete 
b6e251ce53ea: Pull complete 
5c2c99400009: Pull complete 
Digest: sha256:97e9392d12279f8c180eb80f0c7c0f3dfe5650f0f2573f7ad770aea58f75ed12
Status: Downloaded newer image for python:3.13-slim-bookworm
docker.io/library/python:3.13-slim-bookworm

@cardoesnumbers ➜ /workspaces/de_zoomcamp/w1_docker_terraform/w1_homework (main) $ docker run -it --entrypoint bash python:3.13-slim-bookworm
root@6b59de9441d8:/# python --version
Python 3.13.11
root@6b59de9441d8:/# which python
/usr/local/bin/python

root@6b59de9441d8:/# pip list
Package Version
------- -------
pip     25.3 (same)

root@6b59de9441d8:/# cat /etc/os-release
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
VERSION_CODENAME=bookworm
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
root@6b59de9441d8:/# echo 'print("Hola desde  Docker!")' > hello.py                   
root@6b59de9441d8:/# python hello.py
Hola desde  Docker!

root@6b59de9441d8:/# exit
exit



Question 2. Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

- In Docker compose files the containers or services are automatically connected (to the same network) using their service names (pgadmin or db in this case). 
- When it comes to the port data, I get port information is: [port to access in local machine]:[port inside the container]
- Containers inside a (the same?) Docker network will connect to their ports inside the container.

All that accounted pgadmin should use the db (service name) : 5432 (default postgres port).


Question 3. Preparing the data.
- I downloaded the data locally. I loaded the data to the existing ny_taxi database from the walkthrough exercise via notebook. I m not using the chunks method as the data seems managable, around 400k rows?
- I am also using the docker compose file for postgres and pgadmin. Out of curiosity I tried to connect to the database using dBeaver but had issues with the password (?) so I am sticking with pgamin for now. Interested in testing more. 

So: First, start the dock compose with the 2 containers, then add the green taxi to the database via jupyter nb and then proceed to query the data.

from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

path = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"

df_green = pd.read_parquet(path)

df_green.head()

df_green.shape

df_green.to_sql(name='green_taxi', con=engine, if_exists='replace')


Question 3. Counting short trips
For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?

--how many trips had a trip_distance of less than or equal to 1 mile? Answer = 8007

select 
	count(trip_distance)
from
	green_taxi
where 
	lpep_pickup_datetime >= '2025-11-01'
and lpep_pickup_datetime < '2025-12-01' (exclusive of upper bound)   
and trip_distance <= 1;


Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).  Answer = November 14 or 2025-11-14

select
	cast(lpep_pickup_datetime as date) as "day",
	max(trip_distance) as longest_trip
from green_taxi
where trip_distance < 100
group by cast(lpep_pickup_datetime as date), trip_distance
order by trip_distance desc
limit 5

Question 5. Biggest pickup zone.Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025? Answer: East Harlem North

select 
	cast(gt."lpep_pickup_datetime" as DATE) as pickup_date,
	z."Zone",
	round(sum(gt."total_amount"))
from green_taxi gt
left join Zones z on gt."PULocationID" = z."LocationID" 
where cast(gt."lpep_pickup_datetime" as DATE) = '2025-11-18'
group by pickup_date, z."Zone"
order by count(1) DESC
limit 5


Question 6. Largest tip
For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip? Answer: Yorkville West


select
	gt."DOLocationID",
	z."Zone",
	z."service_zone",
	max(gt."tip_amount") as largest_tip
from Zones z
join green_taxi gt 
	on z."LocationID" = gt."DOLocationID"
where
	gt."PULocationID" = 74
--and gt."lpep_pickup_datetime" >= DATE '2025-11-01'
--and gt."lpep_pickup_datetime" <  DATE '2025-12-01' 
-- no need because the records show only November 2025 anyway
group by z."service_zone", gt."PULocationID", gt."DOLocationID", z."Zone"
order by largest_tip DESC
limit 1