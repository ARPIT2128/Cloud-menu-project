// Footer.js
import React from "react";
import { Box, Link, Typography } from "@mui/material";
import GitHubIcon from "@mui/icons-material/GitHub";

const Footer = () => {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "20px",
        backgroundColor: "#000000",
        color: "#fff",
        position: "fixed",
        width: "100%",
        bottom: 0,
      }}
    >
      <Link
        href="https://github.com/ARPIT2128"
        target="_blank"
        rel="noopener"
        sx={{
          display: "flex",
          alignItems: "center",
          color: "#fff",
          textDecoration: "none",
        }}
      >
        <GitHubIcon sx={{ marginRight: "8px", color: "white" }} />
        <Typography variant="body1" style={{ color: "white" }}>
          ARPIT2128
        </Typography>
      </Link>
    </Box>
  );
};

export default Footer;
