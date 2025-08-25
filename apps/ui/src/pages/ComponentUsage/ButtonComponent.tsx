import ImageButton from '../../../../../resources/components/button/ImageBtn'
import LoadingButton from '../../../../../resources/components/Button/LoadingButton'
import AnimateButton from '../../../../../resources/components/button/animatebutton'
import Button from '../../../../../resources/components/button/Button'
import { useState } from 'react'

function ButtonComponent() {
  const [state,setState]=useState("Button Not clicked yet")
  const [buttons]=useState([
    {
      label:"Primary",
      className:"bg-primary text-primary-foreground",
    },
     {
      label:"Secondary",
      className:"bg-secondary text-secondary-foreground",
    },
     {
      label:"Create",
      className:"bg-create  text-create-foreground",
    },
     {
      label:"Update",
      className:"bg-update  text-update-foreground",
    },
     {
      label:"Delete",
      className:"bg-delete text-delete-foreground",
    },
     {
      label:"Warning",
      className:"bg-warning text-warning-foreground",
    },
     {
      label:"Link",
      className:"hover:underline hover:text-update",
    },
  ])

  const [border_buttons]=useState([
    
     {
      label:"Primary",
      className:"border border-primary text-primary",
    },
     {
      label:"Create",
      className:"border border-create  text-create",
    },
     {
      label:"Update",
      className:"border border-update  text-update",
    },
     {
      label:"Delete",
      className:"border border-delete text-delete",
    },
     {
      label:"Warning",
      className:"border border-warning text-warning",
    },
     {
      label:"Link",
      className:"hover:underline hover:text-update",
    },
  ])

  const [border_less_buttons]=useState([
    
     {
      label:"Primary",
      className:"text-primary",
    },
     {
      label:"Create",
      className:"text-create",
    },
     {
      label:"Update",
      className:"text-update",
    },
     {
      label:"Delete",
      className:"text-delete",
    },
     {
      label:"Warning",
      className:"text-warning",
    },
     {
      label:"Link",
      className:"hover:underline hover:text-update",
    },
  ])

  const [icon_buttons] = useState([
  {
    label: "Primary",
    icon: "plus",
    className: "p-2 text-primary-foreground bg-primary",
  },
  {
    label: "Create",
    icon: "edit",
    className: "p-2 text-create-foreground bg-create",
  },
  {
    label: "Update",
    icon: "delete",
    className: "p-2 text-delete-foreground bg-update",
  },
  {
    label: "Delete",
    icon: "view",
   className: "p-2 text-create-foreground bg-create",
  },
  {
    label: "Warning",
    icon: "chevronUp",
  className: "p-2 text-warning-foreground bg-warning",
  },
  {
    label: "Link",
    icon: "chevronDown",
  className: "p-2 text-delete-foreground bg-update",
  },
   {
    label: "Link",
    icon: "search",
   className: "p-2 text-update-foreground bg-create",
  },
   {
    label: "Link",
    icon: "close",
   className: "p-2 text-update-foreground bg-delete",
  },
]);

const [animate_button] = useState([
  {
    label: "Create",
    mode: "create",
    className: "bg-create hover:bg-create",
  },
  {
    label: "Edit",
    mode: "edit",
    className: "bg-edit hover:bg-edit",
  },
  {
    label: "Delete",
    mode: "delete",
    className: "bg-delete hover:bg-delete",
  },
  {
    label: "View",
    mode: "view",
    className: "bg-warning hover:bg-warning",
  },
  
]);

const [loading_button] = useState([
  { label: "Primary", className: "text-primary" },
  { label: "Create", className: "text-create" },
  { label: "Update", className: "text-update" },
  { label: "Delete", className: "text-delete" },
  { label: "Warning", className: "text-warning" },
  { label: "Link", className: "hover:underline hover:text-update" },
]);

  return (
  <div className='pb-20'>
    <h1 className='text-center mb-4 text-2xl'>{state}</h1>

    <div className='flex flex-wrap justify-center gap-3 px-5'>
        {
          buttons.map((button,idx)=>(
            <div key={idx} className='flex flex-row gap-3'>
                <Button label={button.label} className={`${button.className}`} onClick={()=>{setState(`${button.label} Button Clicked`)}} children={undefined} />
            </div>
          ))
        }
    </div>

    <div className='my-10 text-center text-2xl'>Border Buttons</div>
      <div className='flex flex-wrap justify-center gap-3 px-5'>
        {
          border_buttons.map((button,idx)=>(
            <div key={idx} className='flex flex-row gap-3'>
                <Button label={button.label} className={`${button.className}`} onClick={()=>{setState(`${button.label} border Button Clicked`)}} children={undefined} />
            </div>
          ))
        }
    </div>

    <div className='my-10 text-center text-2xl'>Borderless Buttons</div>
      <div className='flex flex-wrap justify-center gap-3 px-5'>
        {
          border_less_buttons.map((button,idx)=>(
            <div key={idx} className='flex flex-row gap-3'>
                <Button label={button.label} className={`${button.className}`} onClick={()=>{setState(`${button.label} border Button Clicked`)}} children={undefined} />
            </div>
          ))
        }
    </div>

    <div className='my-10 text-center text-2xl'>Icon Buttons</div>

        <div className='flex gap-10 justify-center p-5 flex-wrap'>
             {icon_buttons.map((btn, index) => (
            <ImageButton
              key={index}
              icon={btn.icon}
              onClick={()=>{setState(`${btn.label} icon Button Clicked`)}}
              className={btn.className}
            />
          ))}
        </div>

    <div className='my-10 text-center text-2xl'>Loading Buttons</div>

          <div className='flex justify-center gap-5 flex-wrap'>
            
          {loading_button.map((btn, i) => (
            <LoadingButton key={i} className={btn.className}>
              {btn.label}
            </LoadingButton>
          ))}

          </div>

    <div className='my-10 text-center text-2xl'>Animate Buttons</div>


    <div className='flex gap-5 justify-center flex-wrap'>
      {
      animate_button.map((btn)=>(
        <AnimateButton label={btn.label} mode={btn.mode as any} className={btn.className} />
      ))
    }

</div>



  </div>
   
  )
}

export default ButtonComponent