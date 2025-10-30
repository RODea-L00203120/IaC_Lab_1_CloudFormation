import http from 'k6/http';
import { check } from 'k6';

const names = [
  'Alice', 'Bob', 'Charlie', 'David', 'Emma',
  'Frank', 'Grace', 'Henry', 'Iris', 'Jack',
  'Kate', 'Liam', 'Mia', 'Noah', 'Olivia',
  'Peter', 'Quinn', 'Rachel', 'Sam', 'Tina',
  'Uma', 'Victor', 'Wendy', 'Xavier', 'Yara',
  'Zach', 'Amy', 'Ben', 'Clara', 'Dan',
  'Eve', 'Fred', 'Gina', 'Hank', 'Ivy',
  'Joe', 'Kim', 'Leo', 'Maya', 'Nick',
  'Oscar', 'Pam', 'Ray', 'Sue', 'Tom',
  'Val', 'Will', 'Xena', 'Yogi', 'Zoe'
];

const BASE_URL = 'https://sgeb81br8a.execute-api.us-east-1.amazonaws.com/Prod';

export let options = {
  vus: 1,          // 1 virtual user
  iterations: 50,  // 50 total requests
};

export default function () {
  // Pick random name
  const randomName = names[Math.floor(Math.random() * names.length)];
  
  // Test /greeting/{name}
  const res = http.get(`${BASE_URL}/greeting/${randomName}`);
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'has message': (r) => r.json('message') !== undefined,
    'has ip': (r) => r.json('ip') !== undefined,
  });
}