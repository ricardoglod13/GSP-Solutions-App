import React, { useState } from 'react'
import { Link } from 'react-router-dom';

const DropdownComponent = (props) => {
    const [dropdown, setDropdown] = useState(false);

    const dropdownAction = () => {
        setDropdown(!dropdown);
    }

    return (
        <div onClick={dropdownAction} className={`dropdown ${props.dropdownName.class}`}>
            {props.dropdownName.name}
            {dropdown ?( 
                <ul>
                    {props.rutas.map( ruta => 
                        <li>
                            <Link to={`/${ruta.name}`} className={`${ruta.class}`}>{`${ruta.label}`}</Link>
                        </li>
                    )
                    }
                </ul>
                ) : null
            }
        </div>
    );
}

export default DropdownComponent;