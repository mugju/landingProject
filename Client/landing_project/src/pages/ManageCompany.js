import React, {useEffect, useState} from 'react';
import axios from 'axios';

import "./ManageCompany.css";

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
import {Box, IconButton, Modal, Typography} from "@mui/material";

import ClearIcon from '@mui/icons-material/Clear';


const URL = "https://4980c1be-d5e3-4906-a3a7-d989af4b993b.mock.pstmn.io/user";


export default function ManageCompany() {
    const [json, setJson] = useState([]);
    const [rows, setRows] = useState([]);
    // const [json, setJson] = useState(null);
    // const [rows, setRows] = useState(null);

    const [loading, setLoading] = useState(false);

    const [rowCount, setRowCount] = useState(5);
    // const [page, setPage] = useState(1);
    const [pageCount, setPageCount] = useState(10);

    const [currModal, setCurrModal] = useState(0);

    const [open, setOpen] = useState(false);


    const [edit, setEdit] = useState(false);




    const handleOpen = (uid) => {
        setOpen(true);
        setCurrModal(uid);
    }
    const handleClose = () => {
        setOpen(false);
        setEdit(false);
    }






    const fetchUrl = async (url) => {
        const response = await axios.get(url);
        const resData = response.data;
        setJson(resData);
        setRows(resData.slice(0, rowCount));
        setPageCount(Math.ceil(resData.length / rowCount));

        setLoading(true);
    }

    const handleChange = (event, value) => {
        const first = value * rowCount - rowCount;
        const last = value * rowCount;
        const maxLen = json.length;

        setRows(json.slice(first, last > maxLen ? maxLen : last));
    }

    useEffect(() => {
        fetchUrl(URL);
        // handleChange();
        // splitPages(json, 5);
    }, []);


    if (!loading) {
        return null;
    }

    return (
        <>
            <div className="tableContainer">
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
                                    <TableCell align="right"><Button variant="contained" size="small" onClick={() => handleOpen(row.uid)}>View</Button></TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>

                    <Stack className="pContainer" spacing={2}>
                        <Pagination className="pagination" count={pageCount} onChange={handleChange} color="primary" />
                    </Stack>

                </TableContainer>
            </div>



            <Modal
                className="modal"
                open={open}
                onClose={handleClose}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <div className="modalTableContainer">
                    {/*<Button variant="outlined" startIcon={<AccessAlarmOutlinedIcon />}>*/}
                    {/*    Delete*/}
                    {/*</Button>*/}


                    {/*<Button variant="contained" icon={}>Delete</Button>*/}
                    {/*<Button variant="outlined" icon={ClearIcon}>*/}

                    <IconButton aria-label="close" className="iconBtn" onClick={handleClose}>
                        <ClearIcon />
                    </IconButton>

                    {/*<EcoIcon color="primary" />*/}


                    {/*<Home />*/}

                    {edit ? (
                        <TableContainer component={Paper}>
                            <Table aria-label="simple table">
                                <TableBody>
                                    <TableRow>
                                        <TableCell align="right">Name</TableCell>
                                        <TableCell align="right">{json[currModal].comName}</TableCell>
                                    </TableRow>
                                    <TableRow>
                                        <TableCell align="right">License No.</TableCell>
                                        <TableCell align="right">{json[currModal].Licence_No}</TableCell>
                                    </TableRow>
                                    <TableRow>
                                        <TableCell align="right">Address</TableCell>
                                        <TableCell align="right">{json[currModal].address}</TableCell>
                                    </TableRow>
                                    <TableRow>
                                        <TableCell align="right">Contact No.</TableCell>
                                        <TableCell align="right">{json[currModal].contact_No}</TableCell>
                                    </TableRow>
                                    <TableRow>
                                        <TableCell align="right">Email</TableCell>
                                        <TableCell align="right">{json[currModal].email}</TableCell>
                                    </TableRow>
                                    <TableRow>
                                        <TableCell align="right">Description</TableCell>
                                        <TableCell align="right">{json[currModal].description}</TableCell>
                                    </TableRow>
                                </TableBody>
                            </Table>
                        </TableContainer>
                    ) : (
                        <TableContainer component={Paper}>
                            <Table aria-label="simple table">
                                <TableBody>
                                    <TableRow>
                                        <TableCell align="right">aName</TableCell>
                                        <TableCell align="right">{json[currModal].comName}</TableCell>
                                    </TableRow>
                                    <TableRow>
                                        <TableCell align="right">License No.</TableCell>
                                        <TableCell align="right">{json[currModal].Licence_No}</TableCell>
                                    </TableRow>
                                    <TableRow>
                                        <TableCell align="right">Address</TableCell>
                                        <TableCell align="right">{json[currModal].address}</TableCell>
                                    </TableRow>
                                    <TableRow>
                                        <TableCell align="right">Contact No.</TableCell>
                                        <TableCell align="right">{json[currModal].contact_No}</TableCell>
                                    </TableRow>
                                    <TableRow>
                                        <TableCell align="right">Email</TableCell>
                                        <TableCell align="right">{json[currModal].email}</TableCell>
                                    </TableRow>
                                    <TableRow>
                                        <TableCell align="right">Description</TableCell>
                                        <TableCell align="right">{json[currModal].description}</TableCell>
                                    </TableRow>
                                </TableBody>
                            </Table>
                        </TableContainer>
                    )}




                    <Button variant="contained">Delete</Button>
                    <Button variant="contained" onClick={() => setEdit(true)}>Edit</Button>
                    <Button variant="contained">Save</Button>

                </div>
            </Modal>

        </>
    )
}