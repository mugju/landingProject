import React, {useEffect, useState} from 'react';
import axios from 'axios';

import "./Company.css";

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';
import Button from "@mui/material/Button";
import {Box, IconButton, Modal, Typography, TextField, Tooltip, Divider} from "@mui/material";

import ClearIcon from '@mui/icons-material/Clear';
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';


import EditCompany from './EditCompany';
import ViewCompany from './ViewCompany';


const URL = "https://4980c1be-d5e3-4906-a3a7-d989af4b993b.mock.pstmn.io/user";


export default function Company() {
    const [json, setJson] = useState([]);
    const [rows, setRows] = useState([]);

    const [loading, setLoading] = useState(false);

    const [rowCount, setRowCount] = useState(5);
    const [pageCount, setPageCount] = useState(10);

    const [currModal, setCurrModal] = useState(0);

    const [open, setOpen] = useState(false);
    const [edit, setEdit] = useState(false);



    const fetchUrl = async (url) => {
        const response = await axios.get(url);
        const resData = response.data;
        setJson(resData);
        setRows(resData.slice(0, rowCount));
        setPageCount(Math.ceil(resData.length / rowCount));

        setLoading(true);
    }


    const openModal = (uid) => {
        setOpen(true);
        setCurrModal(uid);
    }
    const closeModal = () => {
        setOpen(false);
        setEdit(false);
    }



    const handleChange = (event, value) => {
        const first = value * rowCount - rowCount;
        const last = value * rowCount;
        const maxLen = json.length;

        setRows(json.slice(first, last > maxLen ? maxLen : last));
    }

    useEffect(() => {
        fetchUrl(URL);
    }, []);


    if (!loading) {
        return null; // 로딩중 아이콘 넣기
    }

    return (
        <>
            <div className="tableContainer">
                <div className="titleContainer">
                    <div>Company List</div>
                    <div><Button variant="contained" size="medium">Add Company</Button></div>
                </div>
                <TableContainer component={Paper}>
                    <Table sx={{ minWidth: 650 }} aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell>No.</TableCell>
                                <TableCell align="right">Name</TableCell>
                                <TableCell align="right">License No.</TableCell>
                                <TableCell align="right">Address</TableCell>
                                <TableCell align="right">Contact No.</TableCell>
                                <TableCell align="right">Email</TableCell>
                                <TableCell align="right">Description</TableCell>
                                <TableCell align="right">Added On</TableCell>
                                <TableCell align="right">Action</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {rows.map((row, index) => (
                                <TableRow
                                    key={row.uid}
                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                    <TableCell component="th" scope="row">
                                        {index + 1}
                                    </TableCell>
                                    <TableCell align="right">{row.comName}</TableCell>
                                    <TableCell align="right">{row.Licence_No}</TableCell>
                                    <TableCell align="right">{row.address}</TableCell>
                                    <TableCell align="right">{row.contact_No}</TableCell>
                                    <TableCell align="right">{row.email}</TableCell>
                                    <TableCell align="right">{row.description}</TableCell>
                                    <TableCell align="right">{row.joinDate}</TableCell>
                                    <TableCell align="right"><Button variant="contained" size="small" onClick={() => openModal(row.uid)}>View</Button></TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>

                    <Divider />
                    <Stack className="pContainer" spacing={2}>
                        <Pagination className="pagination" count={pageCount} onChange={handleChange} color="primary" />
                    </Stack>

                </TableContainer>
            </div>



            <Modal
                className="modal"
                open={open}
                onClose={closeModal}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <div className="modalContainer">
                    <div className="btnContainer">
                        <div className='deleteBtn'>
                            <Tooltip title="Delete">
                                <IconButton aria-label="close" className="iconBtn" onClick={() => console.log("delete")}>
                                    <DeleteForeverIcon />
                                </IconButton>
                            </Tooltip>
                        </div>
                        <div className='closeBtn'>
                            <Tooltip title="Close">
                                <IconButton aria-label="close" className="iconBtn" onClick={closeModal}>
                                    <ClearIcon />
                                </IconButton>
                            </Tooltip>
                        </div>
                    </div>
                    
                    {edit ? (
                        <>
                            <EditCompany 
                                key = {currModal}
                                comName = {json[currModal].comName}
                                Licence_No = {json[currModal].Licence_No}
                                address = {json[currModal].address}
                                contact_No = {json[currModal].contact_No}
                                email = {json[currModal].email}
                                description = {json[currModal].description}
                            />
                            <div className="saveBtn">
                                <Button variant="contained" onClick={() => setEdit(false)}>Save</Button>
                            </div>
                        </>
                    ) : (
                        <>
                            <ViewCompany 
                                key = {currModal}
                                comName = {json[currModal].comName}
                                Licence_No = {json[currModal].Licence_No}
                                address = {json[currModal].address}
                                contact_No = {json[currModal].contact_No}
                                email = {json[currModal].email}
                                description = {json[currModal].description}
                            />
                            <div className="editBtn">
                                <Button variant="contained" onClick={() => setEdit(true)}>Edit</Button>
                            </div>
                        </>
                    )}

                </div>
            </Modal>

            {/* <Modal
                className="modal"
                open={open}
                onClose={closeModal}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            ></Modal> */}
        </>
    )
}