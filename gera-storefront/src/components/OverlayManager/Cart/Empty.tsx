import * as React from "react";

import { Button } from "../..";

const Empty: React.FC<{ overlayHide(): void }> = ({ overlayHide }) => (
  <div className="cart__empty">
    <h4>Ihn Warenkorb ist leer</h4>
    <p>
      Sie haben noch nichts Ihrem Warenkorb hinzugefügt. Wir sind sicher das Sie
      noch etwas finden.
    </p>
    <div className="cart__empty__action">
      <Button secondary onClick={overlayHide}>
        Weiter einkaufen
      </Button>
    </div>
  </div>
);

export default Empty;
