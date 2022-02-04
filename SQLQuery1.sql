use MyDB





select (select COMMUNITY_AREA_NAME from dbo.ChicagoCensusData where dbo.ChicagoCensusData.COMMUNITY_AREA_NUMBER = dbo.ChicagoCrimeData.COMMUNITY_AREA_NUMBER)
as COMMUNITY_AREA_NAME
from dbo.ChicagoCrimeData group by COMMUNITY_AREA_NUMBER order by COUNT(DESCRIPTION) desc offset 1 row fetch next 1 rows only




select distinct(PRIMARY_TYPE) from dbo.ChicagoCrimeData where LOCATION_DESCRIPTION like '%school%'






SELECT * FROM dbo.chicagocensusdata




SELECT Elementary_Middle_or_High_School,AVG(safety_score) as Average_Safety_Score FROM dbo.chicagopublicschools
group by Elementary_Middle_or_High_School

