import React, { useState, useEffect } from 'react';
import axios from 'axios';

const EC2Manager = () => {
    const [instances, setInstances] = useState([]);
    const [instanceType, setInstanceType] = useState('t2.micro');
    const [count, setCount] = useState(1);

    const instanceTypes = [
        't2.micro', 't2.small', 't2.medium', 't2.large',
        'm5.large', 'm5.xlarge', 'c5.large', 'r5.large'
    ];

    useEffect(() => {
        fetchInstances();
    }, []);

    const fetchInstances = async () => {
        const response = await axios.get('http://localhost:8000/instances/');
        setInstances(response.data.instances);
    };

    const createInstances = async () => {
        await axios.post('http://localhost:8000/instances/', {
            instance_type: instanceType,
            count: count
        });
        await fetchInstances();
    };

    const destroyInstances = async () => {
        await axios.post('http://localhost:8000/instances/destroy');
        setInstances([]);
    };

    return (
        <div>
            <h2>Manage EC2 Instances</h2>
            
            <div className="controls">
                <select value={instanceType} onChange={(e) => setInstanceType(e.target.value)}>
                    {instanceTypes.map(type => (
                        <option key={type} value={type}>{type}</option>
                    ))}
                </select>
                
                <input 
                    type="number" 
                    value={count} 
                    onChange={(e) => setCount(e.target.value)}
                    min="1"
                    max="5"
                />
                
                <button onClick={createInstances}>Create Instances</button>
                <button onClick={destroyInstances} className="danger">
                    Destroy All Instances
                </button>
            </div>

            <h3>Running Instances</h3>
            <div className="instance-list">
                {instances.map((instance, index) => (
                    <div key={index} className="instance-card">
                        <p>Instance ID: {instance.id}</p>
                        <p>Public IP: {instance.public_ip}</p>
                        <p>State: {instance.state}</p>
                        {instance.public_ip && (
                            <p className="ssh-command">
                                SSH: <code>ssh -i ~/Downloads/insta-test.pem ubuntu@{instance.public_ip}</code>
                            </p>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default EC2Manager;