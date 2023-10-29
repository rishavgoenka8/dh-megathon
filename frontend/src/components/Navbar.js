import React from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Container } from '@mui/material';
import { Link } from 'react-router-dom'; // If you're using React Router

const Navbar = () => {
  return (
    <AppBar position="static">
      <Container maxWidth="lg">
        <Toolbar>
          <Typography variant="h6" component={Link} to="/" style={{ textDecoration: 'none', color: 'white' }}>
            CandidateScope
          </Typography>
          <Button component={Link} to="/" color="inherit">
            Home
          </Button>
          <Button component={Link} to="/dashboard" color="inherit">
            Dashboard
          </Button>
          <Button component={Link} to="/new-application" color="inherit">
            New Application
          </Button>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar;