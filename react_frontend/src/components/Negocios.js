import { Container, Accordion, Badge } from "react-bootstrap";
import Section from "./Section";

const Negocios = ({ negocios, numNota }) => {
  return (
    <Accordion defaultActiveKey="0" flush alwaysOpen>
      {negocios.map((negocio) => {
        return (
          <Accordion.Item
            eventKey={negocio.index}
            key={`${numNota}_${negocio.index}`}
          >
            <Accordion.Header>
              {" "}
              {`${negocio.index + 1}º Negocio`}
            </Accordion.Header>
            <Accordion.Body>
              <h6>
                Mercado Negociado: <b>{negocio.negociacao}</b>
              </h6>
              <h6>
                Compra ou venda: <b>{negocio.cv}</b>
              </h6>
              <h6>
                Categoria do ativo: <b>{negocio.tipo_mercado}</b>
              </h6>
              <h6>
                Nome do ativo: <b>{negocio.nome_pregao}</b>
              </h6>
              <h6>
                Código do ativo: <b>{negocio.codigo}</b>
              </h6>
              <h6>
                Quantidade: <b>{negocio.quantidade}</b>
              </h6>
              <h6>
                Valor unitário:{" "}
                <b>
                  R$
                  {negocio.preco.toLocaleString("pt-br", {
                    minimumFractionDigits: 2,
                  })}
                </b>
              </h6>
              <h6>
                Valor total:{" "}
                <b>
                  R$
                  {negocio.valor_operacao.toLocaleString("pt-br", {
                    minimumFractionDigits: 2,
                  })}
                </b>
              </h6>
              <h6>
                Coberto/Descoberto: <b>{negocio.dc}</b>
              </h6>
            </Accordion.Body>
          </Accordion.Item>
        );
      })}
    </Accordion>
  );
};

export default Negocios;
