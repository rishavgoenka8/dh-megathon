import React, { useEffect, useState } from 'react';
import {
  Table,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Button,
} from '@mui/material';
import { fetchData, postData } from '../service/api';

// Sample data (you'll replace this with data fetched from the backend)
const sampleData = [
  {
    slNo: 1,
    name: 'John Doe',
    linkedin: 'linkedin.com/johndoe',
    twitter: 'twitter.com/johndoe',
    email: 'john@example.com',
    hasReport: true, // Indicates if the data has a report
  },
  {
    slNo: 2,
    name: 'Jane Smith',
    linkedin: 'linkedin.com/janesmith',
    twitter: 'twitter.com/janesmith',
    email: 'jane@example.com',
    hasReport: false,
  },
  // Add more data objects as needed
];

const Dashboard = () => {
  const [data, setData] = useState([]);

  // Simulate fetching data from the backend
  useEffect(() => {
    fetchData('fetch_applicant/')
      .then((responseData) => {
        setData(responseData);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []);

  const handleLaunchReport = (row) => {
    // Handle the "Launch" button click here
    // You can open the report, navigate to a new page, or perform other actions
    // For now, let's log the row data to the console
    console.log('Launching report for:', row.name);
  };

  return (
    <div>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>S.L No.</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>LinkedIn</TableCell>
              <TableCell>Twitter</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Profile Review</TableCell>
              <TableCell>Psychometric Score</TableCell>
              <TableCell>Post Review</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row, index) => (
              <TableRow key={index}>
                <TableCell>{index + 1}</TableCell>
                <TableCell>{row.name}</TableCell>
                <TableCell>{row.linkedIn_url}</TableCell>
                <TableCell>{row.twitter_url !== "" ? row.twitter_url : "N/A"}</TableCell>
                <TableCell>{row.email !== "" ? row.email : "N/A"}</TableCell>
                <TableCell>
                  {row.profile_review !== "" ? (
                    row.profile_review?.split("\n").map((i, key) => {
                      return <div key={key}>{i}</div>;
                    })
                  ) : "In Progress"}
                </TableCell>
                <TableCell>
                  {row.psychometric_score !== "" ? row.psychometric_score : "In Progress"}
                </TableCell>
                <TableCell>
                  {row.post_review !== "" ? (
                    row.post_review?.split("\n").map((i, key) => {
                      return <div key={key}>{i}</div>;
                    })
                  ) : "In Progress"}
                </TableCell>
                {/* <TableCell>
                  {row.hasReport ? (
                    <Button
                      variant="outlined"
                      color="primary"
                      onClick={() => handleLaunchReport(row)}
                    >
                      Launch
                    </Button>
                  ) : (
                    'Creating'
                  )}
                </TableCell> */}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default Dashboard;
