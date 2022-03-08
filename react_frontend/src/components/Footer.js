import React from "react";
import { Navbar, Nav, Container } from "react-bootstrap";
import {
  BsArrowUpCircle,
  BsGithub,
  BsLinkedin,
  BsTwitter,
} from "react-icons/bs";
const Footer = () => {
  return (
    <Navbar variant="primary" bg="dark" className="p-3" fixed="bottom">
      <Container>
        <Navbar.Brand href="#home" className="text-light d-none d-sm-block">
          Desenvolvido por Marcelo Ferraz
        </Navbar.Brand>
        <Nav className="justify-content-between">
          <Nav.Link href="https://twitter.com/Marcelo52304999" target="_blank">
            <BsTwitter size="2em" />
          </Nav.Link>
          <Nav.Link
            href="https://www.linkedin.com/in/marcelo-ferraz-4a349222b/"
            target="_blank"
          >
            <BsLinkedin size="2em" />
          </Nav.Link>
          <Nav.Link
            href="https://github.com/Marcelo-Ferraz-de-Oliveira/controle_aplicacoes_financeiras"
            target="_blank"
          >
            <BsGithub size="2em" />
          </Nav.Link>
        </Nav>
        <Nav className="justify-content-end">
          <Nav.Link href="#top" className="text-success">
            <BsArrowUpCircle size="2em" />
          </Nav.Link>
        </Nav>
      </Container>
    </Navbar>
  );
};

export default Footer;
