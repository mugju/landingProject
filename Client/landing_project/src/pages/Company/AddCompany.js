import React, {useEffect, useState} from 'react';
import {Box, IconButton, Modal, Typography, TextField, Tooltip, Divider, Button, Select, FormControl, InputLabel, MenuItem} from "@mui/material";
import ClearIcon from "@mui/icons-material/Clear";

const generateDate = () => {
    let today = new Date();
    let year = today.getFullYear();
    let month = today.getMonth() + 1;
    let date = today.getDate();

    return (year + '-' + month + '-' + date);
}

export default function AddCompany({ bankList, closeModal }) {
    const [select, setSelect] = useState("");
    const [inputs, setInputs] = useState({
        "com_uid": -1,
        "com_joinDate": generateDate(),
        "com_account_No": "",
        "bank_name": "",
    });

    const handleSelect = (event) => {
        const { name, value } = event.target
        setSelect(value);
        setInputs({
            ...inputs,
            [name]: bankList[value][value + 1]
        })
    };

    const handleChange = (event) => {
        const { id, value } = event.target
        setInputs({
            ...inputs,
            [id]: value
        })
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log(inputs);


        // axios.post("http://local~~", inputs)
        //     .then((res) => {
        //         console.log(res);
        //         closeModal();
        //     })
    };


    return (
        <>
            <div className="modalContainer">
                <div className='closeButton'>
                    <Tooltip title="Close">
                        <IconButton onClick={closeModal}>
                            <ClearIcon />
                        </IconButton>
                    </Tooltip>
                </div>
                <form onSubmit={handleSubmit}>
                    <div className="modalInnerContainer">
                        <div>
                            <div>Name</div>
                            <TextField
                                id="com_name"
                                required
                                label="Required"
                                size="small"
                                onChange={handleChange}
                            />
                            <div>License No.</div>
                            <TextField
                                id="com_licence_no"
                                required
                                label="Required"
                                size="small"
                                onChange={handleChange}
                            />
                            <div>Address</div>
                            <TextField
                                id="com_address"
                                required
                                label="Required"
                                size="small"
                                onChange={handleChange}
                            />
                            <div>Contact No.</div>
                            <TextField
                                id="com_contact_no"
                                required
                                label="Required"
                                size="small"
                                onChange={handleChange}
                            />
                            <div>Email</div>
                            <TextField
                                id="com_email"
                                required
                                label="Required"
                                size="small"
                                onChange={handleChange}
                            />
                            <div>Description</div>
                            <TextField
                                id="com_description"
                                required
                                multiline
                                rows={5}
                                label="Required"
                                size="small"
                                onChange={handleChange}
                            />
                        </div>
                        <div className="modalInnerTitle">
                            Company Bank
                        </div>
                        <div>
                            <div>Account No.</div>
                            <TextField
                                id="com_account_no"
                                size="small"
                                onChange={handleChange}
                            />
                            <div>Bank Name</div>

                            <div>
                                <FormControl fullWidth>
                                    <Select
                                        name="bank_name"
                                        value={select}

                                        onChange={handleSelect}
                                    >
                                        {bankList.map((bank, index) => (
                                            <MenuItem
                                                key={index + 1}
                                                value={index}
                                            >
                                                {bank[index + 1]}
                                            </MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>
                            </div>


                        </div>
                    </div>
                    <div className="saveButton">
                        <Button
                            variant="contained"
                            type="submit"
                        >
                            Save
                        </Button>
                    </div>
                </form>
            </div>
        </>
    )
}