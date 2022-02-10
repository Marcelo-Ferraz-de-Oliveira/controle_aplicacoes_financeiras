import { Container, Accordion, Badge } from "react-bootstrap";

const Negocios = ({ negocios }) => {
  return (
    <Container className="negocios">
      <Accordion defaultActiveKey="0" flush alwaysOpen>
        {negocios.map((negocio) => {
          return (
            <Accordion.Item eventKey={negocio.index}>
              <Accordion.Header> {negocio.index + 1}º Negocio</Accordion.Header>

              <Accordion.Body>
                <h6>
                  Mercado Negociado:{" "}
                  <Badge bg="info">{negocio["Negociação"]}</Badge>
                </h6>
                <h6>
                  Compra ou venda: <Badge bg="info">{negocio["C/V"]}</Badge>
                </h6>
                <h6>
                  Categoria do ativo:{" "}
                  <Badge bg="info">{negocio["Tipo de mercado"]}</Badge>
                </h6>
                <h6>
                  Nome do ativo:{" "}
                  <Badge bg="info">{negocio["Nome Pregão"]}</Badge>
                </h6>
                <h6>
                  Código do ativo: <Badge bg="info">{negocio["Código"]}</Badge>
                </h6>
                <h6>
                  Quantidade: <Badge bg="info">{negocio["Quantidade"]}</Badge>
                </h6>
                <h6>
                  Valor unitário:{" "}
                  <Badge bg="info">
                    R$
                    {negocio["Preço"].toLocaleString("pt-br", {
                      minimumFractionDigits: 2,
                    })}
                  </Badge>
                </h6>
                <h6>
                  Valor total:{" "}
                  <Badge bg="info">
                    R$
                    {negocio["Valor Operação"].toLocaleString("pt-br", {
                      minimumFractionDigits: 2,
                    })}
                  </Badge>
                </h6>
                <h6>
                  Coberto/Descoberto: <Badge bg="info">{negocio["D/C"]}</Badge>
                </h6>
              </Accordion.Body>
            </Accordion.Item>
          );
        })}
      </Accordion>
    </Container>
  );
};

export default Negocios;
