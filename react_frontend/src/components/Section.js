import React from "react";
import { Container } from "react-bootstrap";

const Section = ({ children, bg = "light", text = "dark", flex = "sm" }) => {
  return (
    <section className={`text-center m-2`}>
      <Container
        className={`p-3 bg-light text-dark d-${flex}-flex justify-content-between align-items-center border rounded`}
      >
        {children}
      </Container>
    </section>
  );
};

export default Section;
