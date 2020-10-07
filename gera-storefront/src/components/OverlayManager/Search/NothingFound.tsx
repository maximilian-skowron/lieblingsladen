import * as React from "react";

export const NothingFound: React.FC<{ search: string }> = ({ search }) => (
  <div className="search__products--not-found">
    <p className="u-lead u-lead--bold u-uppercase">
      Kein Produkt vorhanden für: {search}
    </p>
  </div>
);

export default NothingFound;
