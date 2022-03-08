import React from "react";
import Section from "./Section";
import { Container, ListGroup, Form } from "react-bootstrap";
const toBR = (str) => {
  return str.toLocaleString("pt-br", {
    minimumFractionDigits: 2,
  });
};

const Profit = ({ profit, monthProfit }) => {
  return (
    <Section bg="secondary" text="light" flex="md">
      <Container>
        <ListGroup>
          <ListGroup.Item>
            <Form>
              <Form.Select aria-label="Default select example">
                <option value="1">02/2022</option>
                <option value="2">01/2022</option>
                <option value="3">12/2021</option>
              </Form.Select>
            </Form>
          </ListGroup.Item>
          <ListGroup.Item>
            Lucro bruto:{" "}
            <span className="text-info">R${toBR(monthProfit)}</span>
          </ListGroup.Item>
          <ListGroup.Item>
            IR:{" "}
            <span className="text-danger">R${toBR(monthProfit * 0.15)}</span>
          </ListGroup.Item>
          <ListGroup.Item>
            Lucro líquido:{" "}
            <span className="text-warning">R${toBR(monthProfit * 0.85)}</span>
          </ListGroup.Item>
        </ListGroup>
      </Container>
      <Container>
        <ListGroup>
          {Object.entries(profit).map(([data, lucro]) => (
            <ListGroup.Item>
              Lucro no dia {data}: {toBR(lucro)}
            </ListGroup.Item>
          ))}
        </ListGroup>
      </Container>
    </Section>
  );
};

export default Profit;
