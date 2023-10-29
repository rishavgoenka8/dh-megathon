import React, { useEffect, useState } from 'react';
import { fetchData, postData } from '../service/api';
import { Card, CardContent, Typography, Button, TextField, Grid } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import { styled } from '@mui/system';

const RootContainer = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
  height: '100vh', // Full viewport height
});

const CardContainer = styled(Card)({
  width: '80%',
  maxWidth: '400px', // Maximum card width
  padding: '16px',
  textAlign: 'center',
});

const EditButton = styled(Button)({
  marginTop: '16px',
});

function HomePage() {
  const [weights, setWeights] = useState({});
  const [isEditing, setIsEditing] = useState(false);
  const [updatedWeights, setUpdatedWeights] = useState({});

  useEffect(() => {
    fetchData('psychometricweights/')
      .then((responseData) => {
        setWeights(responseData);
        setUpdatedWeights({ ...responseData });
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []);

  const handleEditClick = () => {
    setIsEditing(true);
  };

  const handleSaveClick = () => {
    postData('update_weights/', { weights: updatedWeights })
      .then((response) => {
        console.log('Weights updated successfully:', response);
        setIsEditing(false);
        setWeights(updatedWeights);
      })
      .catch((error) => {
        console.error('Error updating weights:', error);
      });
  };

  const handleWeightChange = (criterion, value) => {
    setUpdatedWeights({ ...updatedWeights, [criterion]: value });
  };

  return (
    <RootContainer style={{ display: 'flex', justifyContent: 'flex-start' }}>
      <CardContainer variant="outlined">
        <CardContent>
          <Typography variant="h3" gutterBottom>
            Psychometric Weights
          </Typography>
          {isEditing ? (
            <div>
              <Typography variant="h5">Edit Weights</Typography>
              <Grid container spacing={4} >
                {Object.keys(updatedWeights).map((criterion) => (
                  <Grid item style={{ width: "200px" }} key={criterion}>
                    <TextField
                      label={criterion}
                      variant="outlined"
                      type="number"
                      value={updatedWeights[criterion]}
                      onChange={(e) => handleWeightChange(criterion, e.target.value)}
                      fullWidth
                    />
                  </Grid>
                ))}
              </Grid>
              <EditButton
                variant="contained"
                color="primary"
                onClick={handleSaveClick}
              >
                Save
              </EditButton>
            </div>
          ) : (
            <div>
              {Object.keys(weights).map((criterion) => (
                <Typography key={criterion} variant="h6">
                  {criterion}: {weights[criterion]}
                </Typography>
              ))}
              <EditButton
                variant="contained"
                color="secondary"
                startIcon={<EditIcon />}
                onClick={handleEditClick}
              >
                Edit
              </EditButton>
            </div>
          )}
        </CardContent>
      </CardContainer>
    </RootContainer>
  );
}

export default HomePage;