$ curl -X POST http://127.0.0.1:4000/api/login   -H "Content-Type: application/json"   -d '{"username":"admin", "password":"admin123"}'
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MzA0MTAyMn0.T730vMDr6TyuOBU0m3KU0e-JeZODe_WHAwe47OFTBok","token_type":"bearer"}

curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MzA0MTAyMn0.T730vMDr6TyuOBU0m3KU0e-JeZODe_WHAwe47OFTBok" http://127.0.0.1:4000/api/protected