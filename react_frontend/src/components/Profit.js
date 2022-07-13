import React from "react";
import Section from "./Section";
import { Container, ListGroup } from "react-bootstrap";

const toBR = (str) => {
  return str.toLocaleString("pt-br", {
    minimumFractionDigits: 2,
  });
};

const Profit = ({ title, monthProfit, monthTaxes }) => {
  return (
    <Section bg="secondary" text="light" flex="md">
      <Container className="row g-4">
        <h4 className="text-center">{title}</h4>
        <Container className="col-md-6 col-lg-3">
          <ListGroup>
            {Object.entries(monthProfit).map(([data, lucro]) => (
              <ListGroup.Item key={data}>
                Lucro no mês {data}: {toBR(lucro)}
              </ListGroup.Item>
            ))}
          </ListGroup>
        </Container>
        <Container className="col-md-6 col-lg-3">
          <ListGroup>
            {Object.entries(monthTaxes).map(([data, lucro]) => (
              <ListGroup.Item key={data}>
                Imposto do mês {data}: {toBR(lucro)}
              </ListGroup.Item>
            ))}
          </ListGroup>
        </Container>
      </Container>
    </Section>
  );
};

export default Profit;
