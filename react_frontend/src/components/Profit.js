import React from "react";
import Section from "./Section";
import { Container, ListGroup, Form } from "react-bootstrap";
import { useState } from "react";

const toBR = (str) => {
  return str.toLocaleString("pt-br", {
    minimumFractionDigits: 2,
  });
};

const Profit = ({ profit, monthProfit }) => {
  const [selectedMonthProfit, setSelectedMonthProfit] = useState(0);
  if (Object.values(monthProfit)[0] && !selectedMonthProfit) {
    setSelectedMonthProfit(Object.values(monthProfit)[0]);
  }
  return (
    <Section bg="secondary" text="light" flex="md">
      <Container className="row g-4">
        <h4 className="text-center">Lucros / Prejuízos</h4>
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
            <ListGroup.Item>
              <Form>
                <Form.Select
                  onChange={(event) =>
                    setSelectedMonthProfit(monthProfit[event.target.value])
                  }
                >
                  {Object.entries(monthProfit).map(([data, lucro]) => (
                    <option value={data} key={data}>
                      {data}
                    </option>
                  ))}
                </Form.Select>
              </Form>
            </ListGroup.Item>
            <ListGroup.Item>
              Lucro bruto:{" "}
              <span className="text-info">R${toBR(selectedMonthProfit)}</span>
            </ListGroup.Item>
            <ListGroup.Item>
              IR:{" "}
              <span className="text-danger">
                R${toBR(selectedMonthProfit * 0.15)}
              </span>
            </ListGroup.Item>
            <ListGroup.Item>
              Lucro líquido:{" "}
              <span className="text-warning">
                R${toBR(selectedMonthProfit * 0.85)}
              </span>
            </ListGroup.Item>
          </ListGroup>
        </Container>
        {/* <Container className="col-md-6 col-lg-3">
          <ListGroup>
            {Object.entries(profit).map(([data, lucro]) => (
              <ListGroup.Item key={data}>
                Lucro no dia {data}: {toBR(lucro)}
              </ListGroup.Item>
            ))}
          </ListGroup>
        </Container> */}
      </Container>
    </Section>
  );
};

export default Profit;
