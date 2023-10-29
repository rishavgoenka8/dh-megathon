import React, { useState } from 'react'; 
import {useNavigate} from "react-router-dom"
import { fetchData, postData } from '../service/api';
import { Container, TextField, Button, Snackbar, Typography, InputLabel, Input } from '@mui/material';
import { styled } from '@mui/system';

const StyledContainer = styled(Container)({
  padding: '16px',
});

const StyledForm = styled('form')({
  display: 'flex',
  flexDirection: 'column',
  gap: '16px',
});

const StyledSubmitButton = styled(Button)({
  marginTop: '16px',
});

const NewApplication = () => {
  const [applicant, setApplicant] = useState({
    name: '',
    linkedin: '',
    twitter: '',
    email: '',
    file: null,
  });
  const navigate = useNavigate();
  const [errors, setErrors] = useState({});
  const [file, setFile] = useState(null);

  const [formErrors, setFormErrors] = useState({});
  const [isSnackbarOpen, setIsSnackbarOpen] = useState(false);

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    const newValue = type === 'file' ? e.target.files[0] : value;

    setApplicant({
      ...applicant,
      [name]: newValue,
    });
    setErrors({ ...errors, [name]: '' });
  };

  const validateForm = () => {
    const newErrors = {};

    if (!applicant.name) {
      newErrors.name = 'Name is required';
    }

    if (!applicant.linkedin) {
      newErrors.email = 'Email is required';
    } else if (!isValidEmail(applicant.linkedin)) {
      newErrors.email = 'Invalid email format';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const isValidEmail = (email) => {
    // Simple email format validation
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
  };

  const handleFileChange = (event) => {
    // Store the selected file
    handleInputChange(event);
    setFile(event.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!applicant.name || !applicant.linkedin || !applicant.file) {
      setIsSnackbarOpen(true);
      return;
    }

    // if (validateForm()) {
      
    // }
    const formData = new FormData();
    formData.append('name', applicant.name);
    formData.append('linkedIn_url', applicant.linkedin);
    formData.append('email', applicant.email);
    formData.append('twitter_url', applicant.twitter);
    formData.append('psychometric_file', file);

    postData('create_applicant/', formData)
      .then((response) => {
        console.log('Applicant created successfully:', response);
        // Clear the form or handle the response as needed
      })
      .catch((error) => {
        console.error('Error creating applicant:', error);
      });
    
    navigate("/dashboard");

    setApplicant({
      name: '',
      linkedin: '',
      twitter: '',
      email: '',
      file: null,
    });
    setFile(null);
  };

  const handleCloseSnackbar = () => {
    setIsSnackbarOpen(false);
  };

  return (
    <StyledContainer>
      <StyledForm onSubmit={handleSubmit}>
        <TextField
          label="Name"
          name="name"
          value={applicant.name}
          onChange={handleInputChange}
          required
          fullWidth
        />
        <TextField
          label="LinkedIn"
          name="linkedin"
          value={applicant.linkedin}
          onChange={handleInputChange}
          required
          fullWidth
        />
        <TextField
          label="Twitter"
          name="twitter"
          value={applicant.twitter}
          onChange={handleInputChange}
          fullWidth
        />
        <TextField
          label="Email"
          name="email"
          value={applicant.email}
          onChange={handleInputChange}
          fullWidth
        />
        <InputLabel>
          Choose a Psychometric Tests and Puzzels file
        </InputLabel>
				<Input
					type="file"
					name="file"
					accept=".csv"
					onChange={handleFileChange}
					required
				/>
        {applicant.file && (
          <Typography variant="body2">
            Selected File: {applicant.file.name}
          </Typography>
        )}
        <StyledSubmitButton
          type="submit"
          variant="contained"
          color="primary"
          disabled={!applicant.name || !applicant.linkedin || !applicant.file}
          onClick={handleSubmit}
        >
          Submit
        </StyledSubmitButton>
      </StyledForm>

      <Snackbar
        open={isSnackbarOpen}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        message="Please fill in the required fields (Name, LinkedIn, and File)."
      />
    </StyledContainer>
  );
};

export default NewApplication;
