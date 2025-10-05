import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch';

const NavBar = () => {
  const navigate = useNavigate();

  return (
    <AppBar position="static" sx={{ background: 'linear-gradient(90deg, #0c1445 0%, #1a1a2e 100%)' }}>
      <Toolbar>
        <RocketLaunchIcon sx={{ mr: 2, color: '#00ff88' }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
          <span style={{ color: '#00ff88' }}>Meteor </span>
          <span style={{ color: '#fff' }}>Madness</span>
        </Typography>
        <Box>
          <Button color="inherit" onClick={() => navigate('/')}>
            Inicio
          </Button>
          <Button color="inherit" onClick={() => navigate('/asteroid-launcher')}>
            Launcher
          </Button>
          <Button color="inherit" onClick={() => navigate('/simulation')}>
            Simulación
          </Button>
          <Button color="inherit" onClick={() => navigate('/risk-analysis')}>
            Análisis de Riesgos
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default NavBar;