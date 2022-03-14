import React from "react";
import { Nav, Navbar, Container } from "react-bootstrap";

const Header = ({ setShowAbout }) => {
  return (
    <Navbar expand="lg" variant="dark" bg="dark" fixed="top" sticky="top">
      <Container>
        <Navbar.Brand href="#top">
          Controle de Aplicações Financeiras
        </Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse className="justify-content-end">
          <Nav className="justify-content-end">
            <Nav.Link href="#" onClick={() => setShowAbout(true)}>
              Sobre
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;
