import React from 'react';

function Item({ item, onRemove }){
    return (
      <div>
        <b>{item.price}</b> <span>({item.volume}) </span>
        <button onClick={() => onRemove(item.code)}> DEL </button>
      </div>
    );
}
function ItemList({ items, onRemove }) {
    return (
      <div>
        {items.map(item => (
          <Item item={item} key={item.code} onRemove={onRemove}/>  // User컴포넌트로 삭제함수 전달
        ))}
      </div>
    );
  }

export default ItemList;